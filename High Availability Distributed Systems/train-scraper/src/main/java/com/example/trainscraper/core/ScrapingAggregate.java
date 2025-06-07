package com.example.trainscraper.core;


import com.example.trainscraper.core.commands.CompleteScrapingCommand;
import com.example.trainscraper.core.commands.FailScrapingCommand;
import com.example.trainscraper.core.commands.RequestScrapingCommand;
import com.example.trainscraper.core.commands.StartScrapingCommand;
import com.example.trainscraper.core.events.ScrapingCompletedEvent;
import com.example.trainscraper.core.events.ScrapingFailedEvent;
import com.example.trainscraper.core.events.ScrapingRequestedEvent;
import com.example.trainscraper.core.events.ScrapingStartedEvent;
import com.example.trainscraper.core.repository.ScrapingStatusRepository;
import jakarta.persistence.Transient;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.axonframework.commandhandling.CommandHandler;
import org.axonframework.config.ConfigurerModule;
import org.axonframework.eventhandling.TrackingEventProcessor;
import org.axonframework.eventhandling.TrackingEventProcessorConfiguration;
import org.axonframework.eventsourcing.EventSourcingHandler;
import org.axonframework.modelling.command.AggregateIdentifier;
import org.axonframework.modelling.saga.SagaLifecycle;
import org.axonframework.spring.stereotype.Aggregate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

import static org.axonframework.modelling.command.AggregateLifecycle.apply;

@Aggregate
@NoArgsConstructor
@Slf4j
public class ScrapingAggregate {

    @AggregateIdentifier
    private UUID scrapingId;

    private int fromStation;
    private int toStation;
    private int numberOfPersons;

    private boolean started;
    private boolean completed;
    private boolean failed;

    @CommandHandler
    public ScrapingAggregate(RequestScrapingCommand cmd, ScrapingStatusRepository repository) {
        // just after controller
        log.info("Received RequestScrapingCommand for {}", cmd.getScrapingId());
        boolean started = repository.existsById(cmd.getScrapingId());
        repository.findById(cmd.getScrapingId())
                .ifPresentOrElse(
                        status -> log.info("status: {}", status.getStatus()),
                        () -> log.info("status: not found for ID {}", cmd.getScrapingId())
                );

        if(started) {
            log.info("Scraping RequestScrapingCommand with this ID already exists: {}", cmd.getScrapingId());
            return;
        }
        apply(new ScrapingRequestedEvent(cmd));
    }

    @EventSourcingHandler
    public void on(ScrapingRequestedEvent event, ScrapingStatusRepository repository) {
        log.info("Applying ScrapingRequestedEvent for {}", event.getScrapingId());

        this.scrapingId = event.getScrapingId();
        this.fromStation = event.getFromStation();
        this.toStation = event.getToStation();
        this.numberOfPersons = event.getNumberOfPersons();
        this.started = false;
        this.completed = false;
        this.failed = false;
    }

    @CommandHandler
    public void handle(StartScrapingCommand cmd, ScrapingStatusRepository repository) {

        boolean started = repository.findById(cmd.getScrapingId())
                .map(s -> !s.getStatus().equals("REQUESTED"))
                .orElse(false);
        repository.findById(cmd.getScrapingId())
                .ifPresentOrElse(
                        status -> log.info("status: {}", status.getStatus()),
                        () -> log.info("status: not found for ID {}", cmd.getScrapingId())
                );

        if(started) {
            log.info("Scraping StartScrapingCommand with this ID already exists: {}", cmd.getScrapingId());
        }
        else{
            log.info("Scraping started for {} in aggregate", cmd.getScrapingId());
            apply(new ScrapingStartedEvent(cmd));
        }
    }

    @EventSourcingHandler
    public void on(ScrapingStartedEvent event) {
        this.started = true;
    }

    @CommandHandler
    public void handle(CompleteScrapingCommand cmd , ScrapingStatusRepository repository) {
        if (!this.started) {
            throw new IllegalStateException("Scraping not started yet.");
        }
       // apply(new ScrapingCompletedEvent(cmd.getScrapingId(), cmd.getResults()));
        log.info("apply completed for {} in aggregate", cmd.getScrapingId());

        log.info("Projecting ScrapingCompletedEvent for");
        log.info("Projecting ScrapingCompletedEvent for {}", cmd.getScrapingId());
        repository.findById(cmd.getScrapingId()).ifPresent(s -> {
            log.info("Before updating, results size: {}", s.getResults().size());
            s.setStatus("COMPLETED");
            s.getResults().clear();
            s.getResults().addAll(cmd.getResults().getResults());

            cmd.getResults().getResults().forEach(j -> j.setScrapingStatus(s));

            repository.saveAndFlush(s);
            log.info("After updating, results size: {}", s.getResults().size());
        });
    }

    @EventSourcingHandler
    public void on(ScrapingCompletedEvent event) {
        log.info("Scraping completed for {} in aggregate", event.getScrapingId());
        this.completed = true;
    }

    @CommandHandler
    public void handle(FailScrapingCommand cmd) {
        if (this.completed) {
            throw new IllegalStateException("Scraping is already completed successfully.");
        }
        apply(new ScrapingFailedEvent(cmd.getScrapingId(), cmd.getReason()));
    }

    @EventSourcingHandler
    public void on(ScrapingFailedEvent event) {
        this.failed = true;
    }
}
