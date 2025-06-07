package com.example.trainscraper.core.data;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class ScrapingStatus {

    @Id
    private UUID scrapingId;

    @Column(length = 15000)
    private String status;

    @OneToMany(mappedBy = "scrapingStatus", cascade = CascadeType.ALL, fetch = FetchType.EAGER,  orphanRemoval = true)
    @JsonManagedReference
    private List<Journey> results = new ArrayList<>();

    private String reason;
}
