package com.devmatch.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.HashSet;
import java.util.Set;

/**
 * Entidad JPA: Project
 * Representa los proyectos disponibles en el sistema
 */
@Entity
@Table(name = "projects")
public class Project {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull(message = "El nombre del proyecto es requerido")
    @Size(min = 1, max = 200, message = "El nombre debe tener entre 1 y 200 caracteres")
    @Column(name = "name", nullable = false, length = 200)
    private String name;
    
    @NotNull(message = "La descripción es requerida")
    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    private String description;
    
    @NotNull(message = "El nivel de experiencia es requerido")
    @Size(max = 50)
    @Column(name = "experience_level", nullable = false, length = 50)
    private String experienceLevel; // Beginner, Intermediate, Advanced
    
    @NotNull(message = "El tipo de proyecto es requerido")
    @Size(max = 50)
    @Column(name = "project_type", nullable = false, length = 50)
    private String projectType; // Web, Mobile, Desktop
    
    @Size(max = 50)
    @Column(name = "status", nullable = false, length = 50)
    private String status = "Open"; // Open, Closed, In Progress
    
    // Relación Many-to-Many con Technologies
    @ManyToMany
    @JoinTable(
        name = "project_technologies",
        joinColumns = @JoinColumn(name = "project_id"),
        inverseJoinColumns = @JoinColumn(name = "technology_id")
    )
    private Set<Technology> requiredTechnologies = new HashSet<>();
    
    // Constructors
    public Project() {}
    
    public Project(String name, String description, String experienceLevel, String projectType) {
        this.name = name;
        this.description = description;
        this.experienceLevel = experienceLevel;
        this.projectType = projectType;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getExperienceLevel() {
        return experienceLevel;
    }
    
    public void setExperienceLevel(String experienceLevel) {
        this.experienceLevel = experienceLevel;
    }
    
    public String getProjectType() {
        return projectType;
    }
    
    public void setProjectType(String projectType) {
        this.projectType = projectType;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public Set<Technology> getRequiredTechnologies() {
        return requiredTechnologies;
    }
    
    public void setRequiredTechnologies(Set<Technology> requiredTechnologies) {
        this.requiredTechnologies = requiredTechnologies;
    }
    
    @Override
    public String toString() {
        return "Project{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", experienceLevel='" + experienceLevel + '\'' +
                ", projectType='" + projectType + '\'' +
                ", status='" + status + '\'' +
                '}';
    }
}
