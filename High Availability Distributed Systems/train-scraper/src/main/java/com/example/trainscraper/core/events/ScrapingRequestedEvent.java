package com.example.trainscraper.core.events;


import com.example.trainscraper.core.commands.RequestScrapingCommand;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor(force = true)
@Getter
public class ScrapingRequestedEvent {
    UUID scrapingId;
    int fromStation;
    int toStation;
    int numberOfPersons;
    LocalDateTime startTime;

    public ScrapingRequestedEvent(RequestScrapingCommand command) {
        this.scrapingId = command.getScrapingId();
        this.fromStation = command.getFromStation();
        this.toStation = command.getToStation();
        this.numberOfPersons = command.getNumberOfPersons();
        this.startTime = command.getStartTime();
    }
}

