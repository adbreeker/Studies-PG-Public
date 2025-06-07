package com.example.trainscraper.core.events;

import com.example.trainscraper.core.commands.StartScrapingCommand;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor(force = true)
public class ScrapingStartedEvent {
    UUID scrapingId;
    int fromStation;
    int toStation;
    int numberOfPersons;
    LocalDateTime startTime;

    public ScrapingStartedEvent(StartScrapingCommand command) {
        this.scrapingId = command.getScrapingId();
        this.fromStation = command.getFromStation();
        this.toStation = command.getToStation();
        this.numberOfPersons = command.getNumberOfPersons();
        this.startTime = command.getStartTime();
    }
}
