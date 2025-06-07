package com.example.trainscraper.core.events;

import com.example.trainscraper.core.data.ScrapingStatus;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor(force = true)
public class ScrapingCompletedEvent {
    UUID scrapingId;
    ScrapingStatus results;
}
