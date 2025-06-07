package com.example.trainscraper.core.commands;

import lombok.AllArgsConstructor;
import lombok.Getter;
import org.axonframework.modelling.command.TargetAggregateIdentifier;


import lombok.Value;
import lombok.NoArgsConstructor;
import org.axonframework.modelling.command.TargetAggregateIdentifier;

import java.time.LocalDateTime;
import java.util.UUID;

@Value
@Getter
@NoArgsConstructor(force = true)
@AllArgsConstructor
public class RequestScrapingCommand {
    @TargetAggregateIdentifier
    UUID scrapingId;
    int fromStation;
    int toStation;
    int numberOfPersons;
   LocalDateTime startTime;


}

