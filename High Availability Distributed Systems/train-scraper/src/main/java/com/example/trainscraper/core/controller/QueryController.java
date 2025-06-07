package com.example.trainscraper.core.controller;


import com.example.trainscraper.core.HardcodedValues;
import com.example.trainscraper.core.data.ScrapingStatus;
import com.example.trainscraper.core.repository.ScrapingStatusRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.codec.json.Jackson2JsonDecoder;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.UUID;

@RestController
@RequestMapping("/api/queries")
@RequiredArgsConstructor
@Slf4j
public class QueryController {

    private final ScrapingStatusRepository repository;

    @Autowired
    private ObjectMapper objectMapper;

    @Transactional(readOnly = true)
    @GetMapping("/scraping/{id}")
    public /*ScrapingStatus*/ String getScrapingStatus(@PathVariable String id) throws JsonProcessingException {
        // hardcoded part
        if(id.equals("5db8dae2-1144-409e-8a3f-8b61a49f8047")) {
            return HardcodedValues.GG_GW;
        } else if (id.equals("4fbcc2db-1794-4e46-81a8-0b8a0d0c717b")) {
            return HardcodedValues.GG_WC;
        } else if (id.equals("0bf0a6c2-69f8-4a71-930b-21e345b40800")) {
            return HardcodedValues.GG_PG;
        } else if (id.equals("b39eabd0-bbbb-46db-abe5-a13303524d11")) {
            return HardcodedValues.GG_KG;
        } else if (id.equals("67372771-5092-4ae0-ab8a-71a7f0ac1d23")) {
            return HardcodedValues.GW_GG;
        } else if (id.equals("201207a4-e5e1-4376-a94d-ccc3c88d65b1")) {
            return HardcodedValues.GW_WC;
        } else if (id.equals("98681aa6-e67a-4495-87f3-10f7561273e9")) {
            return HardcodedValues.GW_PG;
        } else if (id.equals("18cf569d-224a-461a-be51-22bc5af182a1")) {
            return HardcodedValues.GW_KG;
        } else if (id.equals("5b088beb-5244-44f5-a961-21016ba7c536")) {
            return HardcodedValues.WC_GG;
        } else if (id.equals("09883ef8-a05a-4417-a2b6-8eca94f79ca2")) {
            return HardcodedValues.WC_GW;
        } else if (id.equals("0f99120b-075e-4026-bd1e-8cf0aed85038")) {
            return HardcodedValues.WC_PG;
        } else if (id.equals("08748660-b108-4b02-8e21-e02d8b979403")) {
            return HardcodedValues.WC_KG;
        } else if (id.equals("9e87fb2c-a3b6-4cc7-a19f-46c2ece0ee80")) {
            return HardcodedValues.PG_GG;
        } else if(id.equals("f6370395-9f70-4d1f-8f98-5196c9d89716")) {
            return HardcodedValues.PG_GW;
        } else if (id.equals("324a1c21-f990-4a98-b438-d01ff4e7ee7d")) {
            return HardcodedValues.PG_WC;
        } else if (id.equals("a3ea7f83-00c7-482b-bc01-7145d030fb93")) {
            return HardcodedValues.PG_KG;
        } else if (id.equals("5ba6dad4-9abe-4dac-84a8-c73d66482546")) {
            return HardcodedValues.KG_GG;
        } else if (id.equals("8b7a16b1-61b2-4498-bfb0-9f50391f7449")) {
            return HardcodedValues.KG_GW;
        } else if (id.equals("411a8774-9a76-4e30-bcad-a822ecb0b0ee")) {
            return HardcodedValues.KG_WC;
        } else if (id.equals("42a2edcf-69e9-432d-90d4-a596cee1c949")) {
            return HardcodedValues.KG_PG;
        }
        ScrapingStatus status = repository.findById(UUID.fromString(id))
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Scraping status not found"));
        log.info("Querying scraping status for {}: {}", id, status.getResults().size());
        return objectMapper.writeValueAsString(status);
    }

}