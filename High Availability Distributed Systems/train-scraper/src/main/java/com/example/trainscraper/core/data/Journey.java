package com.example.trainscraper.core.data;

import jakarta.persistence.*;
import lombok.*;

import java.util.List;



import com.fasterxml.jackson.annotation.JsonBackReference;


import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonBackReference;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
public class Journey {

    @Id
    @GeneratedValue
    private Long id;

    private String departureScheduled;
    private String departureReal;
    private String arrivalScheduled;
    private String arrivalReal;
    private String travelTime;
    private String price;
    private String trainId;

    // Usuwamy pole availabilityInfo jako string
    // @Column(name = "availability_info", length = 2000)
    // private String availabilityInfo;

    // Dodajemy encję dla sekcji trasy
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "journey_id")
    private List<RouteSection> routeSections = new ArrayList<>();

    @ElementCollection
    private List<String> carriers;

    private boolean delayed;

    @ManyToOne
    @JoinColumn(name = "scraping_id")
    @JsonBackReference
    @ToString.Exclude
    private ScrapingStatus scrapingStatus;
}

