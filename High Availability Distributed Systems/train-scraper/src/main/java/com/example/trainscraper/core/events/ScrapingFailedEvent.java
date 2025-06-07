package com.example.trainscraper.core.events;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor(force = true)
public class ScrapingFailedEvent {
    UUID scrapingId;
    String reason;
}
