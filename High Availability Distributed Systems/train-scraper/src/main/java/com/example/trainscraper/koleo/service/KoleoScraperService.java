package com.example.trainscraper.koleo.service;

import com.example.trainscraper.core.data.Journey;
import com.example.trainscraper.core.data.ScrapingStatus;
import com.example.trainscraper.core.repository.ScrapingStatusRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.springframework.stereotype.Service;

import java.net.MalformedURLException;
import java.net.URL;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
@RequiredArgsConstructor
@Slf4j
public class KoleoScraperService {

    private final static String hub = "http://firefox:4444/wd/hub";//"http://localhost:4444/wd/hub";//;

    public ScrapingStatus scrape(String from, String to, LocalDateTime date) {


        String dateStr = date.format(DateTimeFormatter.ofPattern("yyyy_dd-MM"));
        log.info("Scraping koleo.pl for {} -> {} on {}", from, to, dateStr);

        UUID scrapingId = UUID.randomUUID();

        ScrapingStatus scrapingStatus = new ScrapingStatus();
        scrapingStatus.setScrapingId(scrapingId);
        scrapingStatus.setStatus("REQUESTED");
        scrapingStatus.setResults(new ArrayList<>());

        FirefoxOptions options = new FirefoxOptions();

        WebDriver driver;
        try {
            driver = new RemoteWebDriver(new URL(hub), options);
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
        try {
            String url = "https://koleo.pl/rozklad-pkp/" + from + "/" + to + "/" + dateStr + "/all/all/";
            driver.get(url);
            log.info("Page title: {}", driver.getTitle());
            log.info("URL: {}", url);

            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(1));
            wait.until(ExpectedConditions.presenceOfElementLocated(By.className("has-train-nr")));

            List<WebElement> elements = driver.findElements(By.className("has-train-nr"));
            elements.forEach(WebElement::click);

            wait.until(ExpectedConditions.presenceOfElementLocated(By.className("train-number-details")));

            log.info("Found {} elements with class 'has-train-nr'", elements.size());

            List<Journey> journeys = parseJourneys(elements, scrapingStatus, driver);

            scrapingStatus.setStatus("COMPLETED");
            scrapingStatus.setResults(journeys);


            return scrapingStatus;
        } catch (Exception e) {
            log.error("Error during scraping: {}", e.getMessage(), e);
            scrapingStatus.setStatus("FAILED");
            scrapingStatus.setReason(e.getMessage());
            return scrapingStatus;
        } finally {
            driver.quit();
        }
    }

    private List<Journey> parseJourneys(List<WebElement> connections, ScrapingStatus parentStatus, WebDriver driver) {
        List<Journey> journeys = new ArrayList<>();
        for (WebElement connection : connections) {
            try {

                WebElement connectionHeader = connection.findElement(By.cssSelector(".connection-header.custom-panel"));
                connectionHeader.click();

                // departure
                WebElement departureDiv = connectionHeader.findElement(By.cssSelector("div.time.from"));
                String depScheduled = departureDiv.findElement(By.cssSelector(".scheduled-part")).getText().trim();
                String depReal = null;
                String realTextFrom = departureDiv.findElement(By.cssSelector(".real-time-part")).getText().trim();
                boolean delayed = false;
                if (!realTextFrom.isEmpty() && realTextFrom.matches("\\d{2}:\\d{2}") && !realTextFrom.equals(depScheduled)) {
                    depReal = realTextFrom;
                    delayed = true;
                }

                // arrival
                WebElement arrivalDiv = connectionHeader.findElement(By.cssSelector("div.time.to"));
                String arrScheduled = arrivalDiv.findElement(By.cssSelector(".scheduled-part")).getText().trim();
                String arrReal = null;
                String realTextTo = arrivalDiv.findElement(By.cssSelector(".real-time-part")).getText().trim();
                if (!realTextTo.isEmpty() && realTextTo.matches("\\d{2}:\\d{2}") && !realTextTo.equals(arrScheduled)) {
                    arrReal = realTextTo;
                    delayed = true;
                }

                // travel time
                String travelTime;
                try {
                    WebElement travelTimeElem = connectionHeader.findElement(By.cssSelector(".travel-time-value"));
                    travelTime = travelTimeElem.getText().trim();
                } catch (Exception ex) {
                    // fallback
                    WebElement fallback = connectionHeader.findElement(By.cssSelector("div.small-3.columns.travel-time"));
                    travelTime = fallback.getText().trim();
                }

                // carriers
                List<String> carriers = new ArrayList<>();
                List<WebElement> carrierDivs = connection.findElements(By.cssSelector("div.carrier-name"));
                for (WebElement carrierDiv : carrierDivs) {
                    List<WebElement> spanElements = carrierDiv.findElements(By.tagName("span"));
                    for (WebElement span : spanElements) {
                        String brandText = span.getAttribute("textContent");
                        if (!brandText.isEmpty()) {
                            carriers.add(brandText);
                        } else {
                            String title = span.getAttribute("title");
                            if (title != null && !title.isEmpty()) {
                                carriers.add(title.trim());
                            }
                        }
                    }
                }
                log.info("Carriers: {}", carriers);

                // price
                String price = null;
                try {
                    WebElement priceElem = connectionHeader.findElement(By.cssSelector("span.connection-price span.price-parts"));
                    price = priceElem.getText().trim();
                } catch (Exception ignore) {
                }

                List<String> trainNumbers = null;
                try {
                    connection.click();

                    List<WebElement> trainNumberElements = connection.findElements(By.cssSelector(".train-number-details"));

                    trainNumbers = trainNumberElements.stream().map(
                            e -> {
                                String trainNumber = e.getAttribute("textContent");
                                Pattern p = Pattern.compile("\\d+");
                                Matcher m = p.matcher(trainNumber);
                                if (m.find()) {
                                    return m.group();
                                }
                                return trainNumber;
                            }
                    ).distinct().toList();


                } catch (Exception ignore) {
                }

                String trainId =  String.join(", ", trainNumbers);

                Journey journey = new Journey();
                // journey.id
                journey.setDepartureScheduled(depScheduled);
                journey.setDepartureReal(depReal);
                journey.setArrivalScheduled(arrScheduled);
                journey.setArrivalReal(arrReal);
                journey.setTravelTime(travelTime);
                journey.setCarriers(carriers);
                journey.setPrice(price);
                journey.setDelayed(delayed);
                journey.setTrainId(trainId);

                journey.setScrapingStatus(parentStatus);

                journeys.add(journey);
            } catch (Exception ex) {
                log.debug("Skipping one connection, parse error: {}", ex.getMessage());
            }
        }

        log.info("Parsed {} journeys", journeys.size());
        return journeys;
    }
}
