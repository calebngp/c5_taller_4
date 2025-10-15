package com.devmatch.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.HashSet;
import java.util.Set;

/**
 * Entidad JPA: Technology
 * Representa las tecnologías/habilidades disponibles en el sistema
 */
@Entity
@Table(name = "technologies")
public class Technology {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull(message = "El nombre de la tecnología es requerido")
    @Size(min = 1, max = 100, message = "El nombre debe tener entre 1 y 100 caracteres")
    @Column(name = "name", unique = true, nullable = false, length = 100)
    private String name;
    
    @Size(max = 50, message = "La categoría no puede exceder 50 caracteres")
    @Column(name = "category", length = 50)
    private String category; // backend, frontend, mobile, etc.
    
    // Relación Many-to-Many con Projects
    @ManyToMany(mappedBy = "requiredTechnologies")
    private Set<Project> projects = new HashSet<>();
    
    // Relación Many-to-Many con Developers
    @ManyToMany(mappedBy = "skills")
    private Set<Developer> developers = new HashSet<>();
    
    // Constructors
    public Technology() {}
    
    public Technology(String name, String category) {
        this.name = name;
        this.category = category;
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
    
    public String getCategory() {
        return category;
    }
    
    public void setCategory(String category) {
        this.category = category;
    }
    
    public Set<Project> getProjects() {
        return projects;
    }
    
    public void setProjects(Set<Project> projects) {
        this.projects = projects;
    }
    
    public Set<Developer> getDevelopers() {
        return developers;
    }
    
    public void setDevelopers(Set<Developer> developers) {
        this.developers = developers;
    }
    
    @Override
    public String toString() {
        return "Technology{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", category='" + category + '\'' +
                '}';
    }
}
