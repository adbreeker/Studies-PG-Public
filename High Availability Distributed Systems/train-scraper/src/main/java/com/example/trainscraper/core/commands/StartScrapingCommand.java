package com.example.trainscraper.core.commands;

import com.example.trainscraper.core.events.ScrapingRequestedEvent;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Value;
import org.axonframework.modelling.command.TargetAggregateIdentifier;

import java.time.LocalDateTime;
import java.util.UUID;

@Value
@NoArgsConstructor(force = true)
@AllArgsConstructor
@Getter
public class StartScrapingCommand {
    @TargetAggregateIdentifier
    UUID scrapingId;
    int fromStation;
    int toStation;
    int numberOfPersons;
    LocalDateTime startTime;


    public StartScrapingCommand(ScrapingRequestedEvent event) {
        this.scrapingId = event.getScrapingId();
        this.fromStation = event.getFromStation();
        this.toStation = event.getToStation();
        this.numberOfPersons = event.getNumberOfPersons();
        this.startTime = event.getStartTime();
    }

}
