package com.example.trainscraper.core.data;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

// Nowa encja dla dostępności w danej klasie
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClassAvailability {

    @Id
    @GeneratedValue
    private Long id;

    private String className;
    private String availability;
    private String specialSeatInfo;
}
