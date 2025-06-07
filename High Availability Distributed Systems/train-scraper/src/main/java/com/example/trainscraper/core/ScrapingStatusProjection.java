package com.example.trainscraper.core;

import com.example.trainscraper.core.data.ScrapingStatus;
import com.example.trainscraper.core.events.ScrapingCompletedEvent;
import com.example.trainscraper.core.events.ScrapingFailedEvent;
import com.example.trainscraper.core.events.ScrapingRequestedEvent;
import com.example.trainscraper.core.events.ScrapingStartedEvent;
import com.example.trainscraper.core.repository.ScrapingStatusRepository;
import jakarta.persistence.Transient;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.axonframework.eventhandling.EventHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
@RequiredArgsConstructor
@Slf4j
public class ScrapingStatusProjection {


    @Transactional
    @EventHandler
    public void on(ScrapingRequestedEvent event, ScrapingStatusRepository repository) {
        log.info("Projecting ScrapingRequestedEvent for {}", event.getScrapingId());
        ScrapingStatus status = new ScrapingStatus(event.getScrapingId(), "REQUESTED", null, null);
        repository.saveAndFlush(status);
    }

    @Transactional
    @EventHandler
    public void on(ScrapingStartedEvent event, ScrapingStatusRepository repository) {
        log.info("Projecting ScrapingStartedEvent for {}", event.getScrapingId());
        repository.findById(event.getScrapingId()).ifPresent(s -> {
            s.setStatus("STARTED");
            repository.saveAndFlush(s);
        });
    }
//    @Transactional
//    @EventHandler
//    public void on(ScrapingCompletedEvent event, ScrapingStatusRepository repository) {
//        log.info("Projecting ScrapingCompletedEvent for");
//        log.info("Projecting ScrapingCompletedEvent for {}", event.getScrapingId());
//        repository.findById(event.getScrapingId()).ifPresent(s -> {
//            log.info("Before updating, results size: {}", s.getResults().size());
//            s.setStatus("COMPLETED");
//            s.getResults().clear();
//            s.getResults().addAll(event.getResults().getResults());
//
//            event.getResults().getResults().forEach(j -> j.setScrapingStatus(s));
//
//            repository.saveAndFlush(s);
//            log.info("After updating, results size: {}", s.getResults().size());
//        });
//    }
    @Transactional
    @EventHandler
    public void on(ScrapingFailedEvent event, ScrapingStatusRepository repository) {
        repository.findById(event.getScrapingId()).ifPresent(s -> {
            s.setStatus("FAILED");
            s.setReason(event.getReason());
            repository.saveAndFlush(s);
        });
    }
}

