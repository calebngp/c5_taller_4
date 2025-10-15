package com.devmatch.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/**
 * Entidad JPA: Experience
 * Representa las experiencias laborales/educativas de un desarrollador
 */
@Entity
@Table(name = "experiences")
public class Experience {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull(message = "La descripción es requerida")
    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    private String description;
    
    @Size(max = 100)
    @Column(name = "category", length = 100)
    private String category; // work, education, project, etc.
    
    // Relación Many-to-One con Developer
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "developer_id", nullable = false)
    private Developer developer;
    
    // Constructors
    public Experience() {}
    
    public Experience(String description, String category) {
        this.description = description;
        this.category = category;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getCategory() {
        return category;
    }
    
    public void setCategory(String category) {
        this.category = category;
    }
    
    public Developer getDeveloper() {
        return developer;
    }
    
    public void setDeveloper(Developer developer) {
        this.developer = developer;
    }
    
    @Override
    public String toString() {
        return "Experience{" +
                "id=" + id +
                ", description='" + description + '\'' +
                ", category='" + category + '\'' +
                '}';
    }
}
