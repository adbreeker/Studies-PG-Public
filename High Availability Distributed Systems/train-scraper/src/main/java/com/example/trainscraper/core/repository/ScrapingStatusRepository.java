package com.example.trainscraper.core.repository;

import com.example.trainscraper.core.data.Journey;
import com.example.trainscraper.core.data.ScrapingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

public interface ScrapingStatusRepository extends JpaRepository<ScrapingStatus, UUID> {

    @Modifying
    @Transactional
    @Query("UPDATE ScrapingStatus s SET s.status = :status, s.results = :results WHERE s.scrapingId = :scrapingId")
    void updateStatusAndResults(String scrapingId, String status, List<Journey> results);
}