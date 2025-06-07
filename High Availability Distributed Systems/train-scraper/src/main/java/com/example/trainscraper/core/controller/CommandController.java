package com.example.trainscraper.core.controller;

import com.example.trainscraper.core.HardcodedValues;
import com.example.trainscraper.core.commands.RequestScrapingCommand;
import lombok.RequiredArgsConstructor;
import org.axonframework.commandhandling.gateway.CommandGateway;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.UUID;

@RestController
@RequestMapping("/api/commands")
@RequiredArgsConstructor
public class CommandController {

    private final CommandGateway commandGateway;

    @PostMapping("/scrap")
    public String requestScraping(@RequestParam String from, @RequestParam String to) {
        UUID scrapingId = UUID.randomUUID();

        int fromStation = Integer.parseInt(from);
        int toStation = Integer.parseInt(to);
        //todo
        LocalDateTime startTime = LocalDateTime.now();
        RequestScrapingCommand command = new RequestScrapingCommand(scrapingId, fromStation, toStation, 2, startTime);

        // hardcoded part
        if (fromStation == 40 && toStation == 5162) {
            return "5db8dae2-1144-409e-8a3f-8b61a49f8047";
        } else if (fromStation == 40 && toStation == 242) {
            return "4fbcc2db-1794-4e46-81a8-0b8a0d0c717b";//HardcodedValues.GG_WC;
        } else if (fromStation == 40 && toStation == 159) {
            return "0bf0a6c2-69f8-4a71-930b-21e345b40800";//HardcodedValues.GG_PG;
        } else if (fromStation == 40 && toStation == 85) { //kg
            return "b39eabd0-bbbb-46db-abe5-a13303524d11";//HardcodedValues.GG_KG;
        } else if (fromStation == 5162 && toStation == 40) {
            return "67372771-5092-4ae0-ab8a-71a7f0ac1d23";//HardcodedValues.GW_GG;
        } else if (fromStation == 5162 && toStation == 242) {
            return "201207a4-e5e1-4376-a94d-ccc3c88d65b1";//HardcodedValues.GW_WC;
        } else if (fromStation == 5162 && toStation == 159) {
            return "98681aa6-e67a-4495-87f3-10f7561273e9";//HardcodedValues.GW_PG;
        } else if (fromStation == 5162 && toStation == 85) {
            return "18cf569d-224a-461a-be51-22bc5af182a1";//HardcodedValues.GW_KG;
        } else if (fromStation == 242 && toStation == 40) {
            return "5b088beb-5244-44f5-a961-21016ba7c536";//HardcodedValues.WC_GG;
        } else if (fromStation == 242 && toStation == 5162) {
            return "09883ef8-a05a-4417-a2b6-8eca94f79ca2";//HardcodedValues.WC_GW;
        } else if (fromStation == 242 && toStation == 159) {
            return "0f99120b-075e-4026-bd1e-8cf0aed85038";//HardcodedValues.WC_PG;
        } else if (fromStation == 242 && toStation == 85) {
            return "08748660-b108-4b02-8e21-e02d8b979403";//HardcodedValues.WC_KG;
        } else if (fromStation == 159 && toStation == 40) {
            return "9e87fb2c-a3b6-4cc7-a19f-46c2ece0ee80";//HardcodedValues.PG_GG;
        } else if (fromStation == 159 && toStation == 5162) {
            return "f6370395-9f70-4d1f-8f98-5196c9d89716";//HardcodedValues.PG_GW;
        } else if (fromStation == 159 && toStation == 242) {
            return "324a1c21-f990-4a98-b438-d01ff4e7ee7d";//HardcodedValues.PG_WC;
        } else if (fromStation == 159 && toStation == 85) {
            return "a3ea7f83-00c7-482b-bc01-7145d030fb93";//HardcodedValues.PG_KG;
        } else if (fromStation == 85 && toStation == 40) {
            return "5ba6dad4-9abe-4dac-84a8-c73d66482546";//HardcodedValues.KG_GG;
        } else if (fromStation == 85 && toStation == 5162) {
            return "8b7a16b1-61b2-4498-bfb0-9f50391f7449";//HardcodedValues.KG_GW;
        } else if (fromStation == 85 && toStation == 242) {
            return "411a8774-9a76-4e30-bcad-a822ecb0b0ee";//HardcodedValues.KG_WC;
        } else if (fromStation == 85 && toStation == 159) {
            return "42a2edcf-69e9-432d-90d4-a596cee1c949";//HardcodedValues.KG_PG;
        }


        commandGateway.send(command);


        return scrapingId.toString();
    }
}

