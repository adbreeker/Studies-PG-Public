package com.example.trainscraper.intercity.service;

import com.example.trainscraper.core.data.ClassAvailability;
import com.example.trainscraper.core.data.Journey;
import com.example.trainscraper.core.data.RouteSection;
import com.example.trainscraper.core.data.ScrapingStatus;
import com.example.trainscraper.core.repository.ScrapingStatusRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.openqa.selenium.*;
import org.openqa.selenium.NoSuchElementException;
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
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
@RequiredArgsConstructor
@Slf4j
public class IntercityScraperService {

    private static final String HUB_URL = "http://firefox:4444/wd/hub"; //"http://localhost:4444/wd/hub";//

    public ScrapingStatus scrape(String fromId, String toId, LocalDateTime date) {

        String dateStr = date.format(DateTimeFormatter.ofPattern("yyyy-MM-dd"));
        log.info("Scraping intercity.pl for {} -> {} on {}", fromId, toId, dateStr);

        UUID scrapingId = UUID.randomUUID();

        ScrapingStatus scrapingStatus = new ScrapingStatus();
        scrapingStatus.setScrapingId(scrapingId);
        scrapingStatus.setStatus("REQUESTED");
        scrapingStatus.setResults(new ArrayList<>());

        FirefoxOptions options = new FirefoxOptions();
        WebDriver driver;

        try {
            driver = new RemoteWebDriver(new URL(HUB_URL), options);
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }

        try {
            // todo hardcoded
            String url = "https://ebilet.intercity.pl/wyszukiwanie?dwyj=" + dateStr + "&swyj=" + fromId + "&sprzy=" + toId + "&polbez=0&polnaj=0&lpol=0&kpoc=EIP&kpoc=EIC&kpoc=IC&kpoc=TLK&kpoc=ZKA&cmax=1440&cmin=3&brail=0&przy=0&time=10:13&ticket50=&ticket100=1010";
            log.info(url);
            driver.get(url);

            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));

            By mainListLocator = By.xpath("//ul[contains(@class, 'YourTrip_yourTrip__container__')]");

            wait.until(ExpectedConditions.presenceOfElementLocated(mainListLocator));

            log.info("journey list found");


            List<WebElement> tripElements = driver.findElements(By.cssSelector("ul[class*='YourTrip_yourTrip__container__'] li[data-testid='TripPropositionDesktop']"));
            log.info("found {} elements of TripPropositionDesktop", tripElements.size());

            List<Journey> journeys = parseTrips(tripElements, driver, wait, scrapingStatus);

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

    private List<Journey> parseTrips(List<WebElement> tripElements, WebDriver driver, WebDriverWait wait, ScrapingStatus parentStatus) {
        List<Journey> journeys = new ArrayList<>();

        for (WebElement tripEl : tripElements) {
            try {
                Journey journey = new Journey();
                journey.setScrapingStatus(parentStatus);

                List<WebElement> timeSpans = tripEl.findElements(By.cssSelector(".TripPropositionDesktop_tripPropositionDesktop__label_bigText__rpnhJ span"));
                if (timeSpans.size() >= 2) {
                    String dep = timeSpans.get(0).getText().trim();
                    String arr = timeSpans.get(1).getText().trim();
                    journey.setDepartureScheduled(dep);
                    journey.setArrivalScheduled(arr);
                }

                try {
                    WebElement travelTimeEl = tripEl.findElement(By.cssSelector(".TripPropositionDesktop_tripPropositionDesktop__label_blueText__SFrag span"));
                    String travelTimeRaw = travelTimeEl.getText().replace("Travel time: ", "").trim();
                    journey.setTravelTime(travelTimeRaw);
                } catch (NoSuchElementException ex) {
                    journey.setTravelTime(null);
                }

                List<String> stations = new ArrayList<>();
                List<WebElement> stationEls = tripEl.findElements(By.cssSelector(".TripPropositionDesktop_tripPropositionDesktop__stationParagraph__bg1nP"));
                for (WebElement stationEl : stationEls) {
                    stations.add(stationEl.getText().trim());
                }

                List<String> carriers = new ArrayList<>();
                List<WebElement> brandElems = tripEl.findElements(By.cssSelector(".TripPropositionDesktop_smallPrintFont__xEVBY"));
                for (WebElement brand : brandElems) {
                    log.info("Brand: {}", brand.getText());
                    String trainNumber = brand.getText().trim();
                    if (!trainNumber.isEmpty()) {
                        Pattern p = Pattern.compile("\\d+");
                        Matcher m = p.matcher(trainNumber);

                        if (m.find()) {
                            trainNumber = m.group();
                            log.info("Train number: {}", trainNumber);
                        }
                        carriers.add(trainNumber);
                    }
                }

                journey.setTrainId(String.join(", ", carriers));

                List<String> trainCarriers = new ArrayList<>();

                List<WebElement> carrierElements = tripEl.findElements(By.cssSelector("svg[aria-label='InterCity'], svg[aria-label='Express InterCity Premium'], svg[aria-label='Twoje Linie Kolejowe']"));
                for (WebElement carrierElement : carrierElements) {
                    log.info("Found carrier element with aria-label: {}", carrierElement.getAttribute("aria-label"));

                    try {
                        String carrier = carrierElement.getAttribute("aria-label");

                        if (carrier != null && !carrier.isEmpty()) {
                            if (carrier.equals("InterCity")) {
                                carrier = "IC";
                            } else if (carrier.equals("Express InterCity Premium")) {
                                carrier = "EIP";
                            } else if (carrier.equals("Twoje Linie Kolejowe")) {
                                carrier = "TLK";
                            }
                            trainCarriers.add(carrier);
                        }
                    } catch (Exception e) {
                        log.error("Error extracting carrier info: {}", e.getMessage());
                    }
                }
                // somehow list contains duplicates
                int halfLength = trainCarriers.size() / 2;
                List<String> firstHalfCarriers = trainCarriers.subList(0, halfLength);
                log.info("Found train carriers: {}", firstHalfCarriers);
                journey.setCarriers(firstHalfCarriers);


                Map<String, String> prices = new LinkedHashMap<>();
                List<WebElement> priceBlocks = tripEl.findElements(By.cssSelector("li[class*='TripPropositionDesktop_tripPropositionDesktop__container_flexColumn__VSV']"));
                for (WebElement pb : priceBlocks) {
                    try {
                        WebElement labelEl = pb.findElement(By.cssSelector(".TripPropositionDesktop_tripPropositionDesktop__label_blueText__SFrag span"));
                        String label = labelEl.getText().trim();

                        WebElement valEl;
                        try {
                            valEl = pb.findElement(By.cssSelector(".TripPropositionDesktop_tripPropositionDesktop__label_bigText__rpnhJ span"));
                        } catch (Exception e) {
                            // if no price, try to find disabled text
                            valEl = pb.findElement(By.cssSelector(".TripPropositionDesktop_tripPropositionDesktop__label_disabledText__xLX2V span"));
                        }

                        String val = valEl.getText().trim();
                        prices.put(label, val);
                        log.info("Price: {} - {}", label, val);
                    } catch (Exception e) {
                        log.error("Error processing price block: {}", e.getMessage());
                    }
                }

                // only second class
                String price = prices.get("Class 2");
                if (price.equals("Unavailable")) {
                    price = prices.get("Class 1");
                }

                journey.setPrice(price);


                WebElement btn = tripEl.findElement(By.cssSelector("button.Accordion_header__rCWpQ.Accordion_headerUnderlined__6zv2L"));

                if (btn != null) {
                    try {
                        btn.click();
                        wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(".Accordion_contentWrapper__DlwUR .CheckAvailableSeats_container__MzE9A")));
                        String seatInfo = parseSeatAvailability(tripEl);
                        log.info("Seat info: {}", seatInfo);
                        //journey.setAvailabilityInfo((journey.getAvailabilityInfo() == null ? "" : journey.getAvailabilityInfo() + "\n") + seatInfo);
                        parseAvailabilityInfo(journey, seatInfo);
                    } catch (Exception ex) {
                        log.debug("error while checking avaibility: {}", ex.getMessage());
                    }
                }

                journeys.add(journey);

            } catch (Exception e) {
                log.debug("Skipping one trip element, parse error: {}", e.getMessage());
            }

        }
        log.info("Parsed {} journeys", journeys.size());
        return journeys;
    }

    private String parseSeatAvailability(WebElement tripEl) {
        List<WebElement> seatSections = tripEl.findElements(By.cssSelector(".Accordion_contentWrapper__DlwUR .CheckAvailableSeats_container__MzE9A .AvailableSeats_grid__nzcvK"));
        StringBuilder sb = new StringBuilder();
        for (WebElement section : seatSections) {
            try {
                WebElement stationRow = section.findElement(By.cssSelector(".AvailableSeats_stations_row__GrQuI"));
                String stationsText = stationRow.getText().replace("\n", " -> ");
                sb.append("section of route: ").append(stationsText).append("\n");

                List<WebElement> infoRows = section.findElements(By.cssSelector(".AvailableSeats_grid_item_wrapper__LBYGR"));
                for (WebElement row : infoRows) {
                    String text = row.getText().trim().replace("\n", " | ");
                    sb.append("   ").append(text).append("\n");
                }
            } catch (Exception ex) {
                log.debug("error in parseSeatAvailability: {}", ex.getMessage());
            }
        }
        return sb.toString();
    }

    public void parseAvailabilityInfo(Journey journey, String input) {
        // Podziel tekst na sekcje
        String[] sectionsRaw = input.split("section of route:");

        List<RouteSection> routeSections = new ArrayList<>();

        for (String secRaw : sectionsRaw) {
            secRaw = secRaw.trim();
            if (secRaw.isEmpty()) continue;

            String[] lines = secRaw.split("\n");

            String routeLine = lines[0].trim().replace("$Section -> ", "");

            RouteSection routeSection = RouteSection.builder()
                    .sectionName(routeLine)
                    .classAvailabilities(new ArrayList<>())
                    .build();

            for (int i = 1; i < lines.length; i++) {
                String line = lines[i].trim();
                if (line.isEmpty()) continue;

                String[] parts = line.split("\\|");
                if (parts.length < 2) continue;

                String className = parts[0].trim();
                String availability = parts[1].trim();
                String specialSeatInfo = parts.length > 2 ? parts[2].trim().replace("A special seat is available: ", "") : "";

                ClassAvailability classAvailability = ClassAvailability.builder()
                        .className(className)
                        .availability(availability)
                        .specialSeatInfo(specialSeatInfo)
                        .build();

                routeSection.getClassAvailabilities().add(classAvailability);
            }

            routeSections.add(routeSection);
        }

        journey.setRouteSections(routeSections);
    }
}



