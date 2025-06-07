package com.example.trainscraper.core.service;

import com.example.trainscraper.core.data.Journey;
import com.example.trainscraper.core.data.ScrapingStatus;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class JourneyGroupingService {

    /**
     * Groups and merges journey results from multiple scraping sources by trainId
     */
    public List<Journey> groupAndMergeJourneys(ScrapingStatus koleoStatus, ScrapingStatus blikomStatus, ScrapingStatus intercityStatus) {
        Map<String, Journey> journeyMap = new HashMap<>();

        addJourneysToMap(koleoStatus, journeyMap);
        addJourneysToMap(blikomStatus, journeyMap);
        addJourneysToMap(intercityStatus, journeyMap);

        return new ArrayList<>(journeyMap.values());
    }

    private void addJourneysToMap(ScrapingStatus status, Map<String, Journey> journeyMap) {
        if (status == null || status.getResults() == null) {
            return;
        }

        for (Journey journey : status.getResults()) {
            if (journey.getTrainId() == null) {
                continue;
            }

            if (journeyMap.containsKey(journey.getTrainId())) {
                updateJourney(journeyMap.get(journey.getTrainId()), journey);
            } else {
                journeyMap.put(journey.getTrainId(), journey);
            }
        }
    }

    private void updateJourney(Journey target, Journey source) {
        if (source.getDepartureScheduled() != null) {
            target.setDepartureScheduled(source.getDepartureScheduled());
        }

        if (source.getDepartureReal() != null) {
            target.setDepartureReal(source.getDepartureReal());
        }

        if (source.getArrivalScheduled() != null) {
            target.setArrivalScheduled(source.getArrivalScheduled());
        }

        if (source.getArrivalReal() != null) {
            target.setArrivalReal(source.getArrivalReal());
        }

        if (source.getTravelTime() != null) {
            target.setTravelTime(source.getTravelTime());
        }

        if (source.getPrice() != null) {
            target.setPrice(source.getPrice());
        }

        if (source.getRouteSections() != null) {
            target.setRouteSections(source.getRouteSections());
        }

        if (source.isDelayed()) {
            target.setDelayed(true);
        }

        if (source.getCarriers() != null) {
            if (target.getCarriers() == null) {
                target.setCarriers(new ArrayList<>());
            }

            for (String carrier : source.getCarriers()) {
                if (!target.getCarriers().contains(carrier)) {
                    target.getCarriers().add(carrier);
                }
            }
        }
    }
}
