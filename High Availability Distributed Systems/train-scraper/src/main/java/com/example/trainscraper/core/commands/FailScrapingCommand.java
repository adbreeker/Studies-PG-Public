package com.example.trainscraper.core.commands;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Value;
import org.axonframework.modelling.command.TargetAggregateIdentifier;

import java.util.UUID;

@Value
@NoArgsConstructor(force = true)
@AllArgsConstructor
@Getter
public class FailScrapingCommand {
    @TargetAggregateIdentifier
    UUID scrapingId;
    String reason;
}
