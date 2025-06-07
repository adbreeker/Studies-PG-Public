package com.example.trainscraper.core.commands;

import com.example.trainscraper.core.data.ScrapingStatus;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Value;
import org.axonframework.modelling.command.TargetAggregateIdentifier;

import java.util.UUID;

@Value
@Getter
@NoArgsConstructor(force = true)
@AllArgsConstructor
public class CompleteScrapingCommand {
    @TargetAggregateIdentifier
    UUID scrapingId;
    ScrapingStatus results;
}
