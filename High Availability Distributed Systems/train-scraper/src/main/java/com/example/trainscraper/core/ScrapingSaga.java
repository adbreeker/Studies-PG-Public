package com.example.trainscraper.core;

import com.example.trainscraper.blikom.service.BlikomScraperService;
import com.example.trainscraper.core.data.ScrapingStatus;
import com.example.trainscraper.core.commands.CompleteScrapingCommand;
import com.example.trainscraper.core.commands.FailScrapingCommand;
import com.example.trainscraper.core.commands.StartScrapingCommand;
import com.example.trainscraper.core.events.ScrapingCompletedEvent;
import com.example.trainscraper.core.events.ScrapingFailedEvent;
import com.example.trainscraper.core.events.ScrapingRequestedEvent;
import com.example.trainscraper.core.events.ScrapingStartedEvent;
import com.example.trainscraper.core.repository.ScrapingStatusRepository;
import com.example.trainscraper.core.service.JourneyGroupingService;
import com.example.trainscraper.core.utils.StationFormatter;
import com.example.trainscraper.intercity.service.IntercityScraperService;
import com.example.trainscraper.koleo.service.KoleoScraperService;
import jakarta.persistence.Transient;
import lombok.extern.slf4j.Slf4j;
import org.axonframework.commandhandling.gateway.CommandGateway;
import org.axonframework.config.EventProcessingConfigurer;
import org.axonframework.modelling.saga.EndSaga;
import org.axonframework.modelling.saga.SagaEventHandler;
import org.axonframework.modelling.saga.SagaLifecycle;
import org.axonframework.modelling.saga.StartSaga;
import org.axonframework.spring.stereotype.Saga;
import org.springframework.beans.factory.annotation.Autowired;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Objects;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@Saga
@Slf4j
public class ScrapingSaga {

    @Autowired
    @Transient
    private transient CommandGateway commandGateway;

    @Autowired
    public void configure(EventProcessingConfigurer configurer) {
        configurer.usingSubscribingEventProcessors();
    }


    @StartSaga
    @SagaEventHandler(associationProperty = "scrapingId")
    public void on(ScrapingRequestedEvent event) {
        log.info("Saga started for {}", event.getScrapingId());

        commandGateway.send(new StartScrapingCommand(event));
    }

    @SagaEventHandler(associationProperty = "scrapingId")
    public void on(ScrapingStartedEvent e, KoleoScraperService koleoScraperService, BlikomScraperService blikomScraperService, IntercityScraperService intercityScraperService, JourneyGroupingService journeyGroupingService, ScrapingStatusRepository repository) {

        int k90from = e.getFromStation();
        int k90to = e.getToStation();
        List<String> from = StationFormatter.namesFormatted(k90from);
        List<String> to = StationFormatter.namesFormatted(k90to);

        log.info("Scraping started for {}", e.getScrapingId());
        repository.findById(e.getScrapingId())
                .ifPresentOrElse(
                        status -> log.info("status: {}", status.getStatus()),
                        () -> log.info("status: not found for ID {}", e.getScrapingId())
                );
        boolean started = repository.findById(e.getScrapingId()).map(s -> !s.getStatus().equals("STARTED")).orElse(false);
        if (started) {
            log.info("Scraping with this ID already started: {}, scraping sag ", e.getScrapingId());
            return;
        }
        try {

            ScrapingStatus koleoStatus = koleoScraperService.scrape(from.get(StationFormatter.KOLEO_IDX), to.get(StationFormatter.KOLEO_IDX), e.getStartTime());
            ScrapingStatus blikomStatus = blikomScraperService.scrape(from.get(StationFormatter.BLIKOM_IDX), to.get(StationFormatter.BLIKOM_IDX), e.getStartTime());
            ScrapingStatus intercityStatus = intercityScraperService.scrape(from.get(StationFormatter.INTERCITY_IDX), to.get(StationFormatter.INTERCITY_IDX), e.getStartTime()); //40, 145;


            boolean isSuccessful = Objects.equals(koleoStatus.getStatus(), "COMPLETED") || Objects.equals(blikomStatus.getStatus(), "COMPLETED") || Objects.equals(intercityStatus.getStatus(), "COMPLETED");

            ScrapingStatus mergedStatus = new ScrapingStatus();
            mergedStatus.setStatus(isSuccessful ? "COMPLETED" : "FAILED");
            mergedStatus.setResults(journeyGroupingService.groupAndMergeJourneys(koleoStatus, blikomStatus, intercityStatus));
            log.info("after scraping, results size: {}", mergedStatus.getResults().size());
            commandGateway.sendAndWait(new CompleteScrapingCommand(e.getScrapingId(), mergedStatus));
        } catch (Exception ex) {
            log.error("Error scraping page: {}", ex.getMessage());
            commandGateway.sendAndWait(new FailScrapingCommand(e.getScrapingId(), ex.getMessage()));
        }


    }


    @EndSaga
    @SagaEventHandler(associationProperty = "scrapingId")
    public void on(ScrapingCompletedEvent event) {
        log.info("Scraping completed. Saga ends for {}", event.getScrapingId());
    }

    @EndSaga
    @SagaEventHandler(associationProperty = "scrapingId")
    public void on(ScrapingFailedEvent event) {
        log.info("Scraping failed. Saga ends for {}", event.getScrapingId());
    }
}
