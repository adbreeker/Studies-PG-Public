package com.example.trainscraper.blikom.service;


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
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class BlikomScraperService {

    private final static String hub = "http://firefox:4444/wd/hub";//"http://localhost:4444/wd/hub";

    public ScrapingStatus scrape(String from, String to, LocalDateTime date) {
        String formattedDate = date.format(DateTimeFormatter.ofPattern("ddMMyyyyHHmm"));

        log.info("Scraping bilkom.pl for {} -> {} on {}", from, to, date);

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
            log.error("Error during initialization of RemoteWebDriver: {}", e.getMessage(), e);
            throw new RuntimeException(e);
        }


        try {
            String url = "https://bilkom.pl/podroz?poczatkowa=O%3D" + from + "&docelowa=O%3D" + to + "&data=" + formattedDate + "&bilkomAvailOnly=on";
            driver.get(url);
            log.info("url: {}", url);
            log.info("Page title: {}", driver.getTitle());

            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
            wait.until(ExpectedConditions.presenceOfElementLocated(By.id("trips")));
            wait.until(d -> {
                List<WebElement> elements = d.findElements(By.cssSelector("span.price[data-toggle='tooltip']"));
                List<WebElement> nonprice = d.findElements(By.cssSelector("span.text.disabled"));
                boolean allDisplayed = elements.stream().allMatch(WebElement::isDisplayed) && nonprice.stream().allMatch(WebElement::isDisplayed);
                return elements.size() + nonprice.size() == 6 && allDisplayed ? elements : null;
            });


            List<WebElement> liElements = driver.findElements(By.cssSelector("#trips li.el"));
            log.info("Found {} elements with class 'el' inside #trips", liElements.size());

            List<Journey> journeys = parseJourneys(liElements, scrapingStatus);

            scrapingStatus.setStatus("COMPLETED");
            scrapingStatus.setResults(journeys);

            return scrapingStatus;
        } catch (Exception e) {
            log.error("Error during scraping Bilkom: {}", e.getMessage(), e);
            scrapingStatus.setStatus("FAILED");
            scrapingStatus.setReason(e.getMessage());
            return scrapingStatus;
        } finally {
            driver.quit();
        }
    }

    private List<Journey> parseJourneys(List<WebElement> connections, ScrapingStatus parentStatus) {
        List<Journey> journeys = new ArrayList<>();

        for (WebElement connection : connections) {
            try {
                List<WebElement> timeElems = connection.findElements(By.cssSelector(".connection-info .date-time .time"));
                if (timeElems.size() < 2) {
                    log.debug("Skipping - not enough time elements found");
                    continue;
                }
                String departureTime = timeElems.get(0).getText().trim(); // np. "09:46"
                String arrivalTime = timeElems.get(1).getText().trim();   // np. "12:30"

                boolean delayed = false;
                for (WebElement t : timeElems) {
                    String classAttr = t.getAttribute("class");
                    if (classAttr != null && classAttr.contains("late")) {
                        delayed = true;
                        break;
                    }
                }

                WebElement durationElem = connection.findElement(By.cssSelector(".arrow .duration"));
                String travelTime = durationElem.getText().trim(); // e.g. "02h44'"


                List<WebElement> carrierWebElementList = connection.findElements(By.cssSelector(".mobile-carrier.carrier-metadata"));
                List<String> carriers = carrierWebElementList.stream().map(WebElement::getText).toList();

                String price = null;
                try {
                    WebElement priceElem = connection.findElement(By.cssSelector(".buy-tickets-wrapper__priceWrapper .price"));
                    price = priceElem.getText().trim();
                } catch (Exception ex) {
                    try {
                        WebElement disabledElem = connection.findElement(By.cssSelector(".buy-tickets-wrapper .text.disabled"));
                        price = disabledElem.getText().trim();
                    } catch (Exception ignored) {
                    }
                }

                // train id
                List<String> trainNumbers = carriers.stream().map(trainNumber -> {
                    Pattern p = Pattern.compile("\\d+");
                    Matcher m = p.matcher(trainNumber);
                    if (m.find()) {
                        return m.group();
                    }
                    return trainNumber;
                }).toList();
                carriers = carriers.stream().map(s -> s.replaceAll("\\d+", "").replaceAll(" ", "").trim()).filter(
                        s -> !s.isEmpty()
                ).toList();

                String trainId = trainNumbers.stream().filter(s -> s != null && !s.isEmpty()).collect(Collectors.joining(", "));


                Journey journey = new Journey();
                journey.setDepartureScheduled(departureTime);
                journey.setDepartureReal(null);
                journey.setArrivalScheduled(arrivalTime);
                journey.setArrivalReal(null);
                journey.setTrainId(trainId);
                journey.setTravelTime(travelTime);
                journey.setCarriers(carriers);
                journey.setPrice(price);
                journey.setDelayed(delayed);

                journey.setScrapingStatus(parentStatus);

                journeys.add(journey);
            } catch (Exception ex) {
                log.debug("Skipping one connection, parse error: {}", ex.getMessage());
            }
        }

        log.info("Parsed {} journeys from Bilkom", journeys.size());
        return journeys;
    }

}
