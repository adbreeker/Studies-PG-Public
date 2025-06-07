package com.example.trainscraper.core.data;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

// Nowa encja dla sekcji trasy
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RouteSection {

    @Id
    @GeneratedValue
    private Long id;

    private String sectionName;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "route_section_id")
    private List<ClassAvailability> classAvailabilities = new ArrayList<>();
}
