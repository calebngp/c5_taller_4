package com.devmatch.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.HashSet;
import java.util.Set;

/**
 * Entidad JPA: Developer
 * Representa los desarrolladores registrados en el sistema
 */
@Entity
@Table(name = "developers")
public class Developer {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull(message = "El nombre es requerido")
    @Size(min = 1, max = 100, message = "El nombre debe tener entre 1 y 100 caracteres")
    @Column(name = "name", nullable = false, length = 100)
    private String name;
    
    @Email(message = "Formato de email inválido")
    @Size(max = 100)
    @Column(name = "email", unique = true, length = 100)
    private String email;
    
    @Size(max = 50)
    @Column(name = "experience_level", length = 50)
    private String experienceLevel; // Beginner, Intermediate, Advanced
    
    @Column(name = "bio", columnDefinition = "TEXT")
    private String bio;
    
    @Size(max = 200)
    @Column(name = "location", length = 200)
    private String location;
    
    @Size(max = 100)
    @Column(name = "github_profile", length = 100)
    private String githubProfile;
    
    // Relación Many-to-Many con Technologies (habilidades del desarrollador)
    @ManyToMany
    @JoinTable(
        name = "developer_skills",
        joinColumns = @JoinColumn(name = "developer_id"),
        inverseJoinColumns = @JoinColumn(name = "technology_id")
    )
    private Set<Technology> skills = new HashSet<>();
    
    // Relación One-to-Many con Experiences
    @OneToMany(mappedBy = "developer", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<Experience> experiences = new HashSet<>();
    
    // Constructors
    public Developer() {}
    
    public Developer(String name, String email, String experienceLevel) {
        this.name = name;
        this.email = email;
        this.experienceLevel = experienceLevel;
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
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public String getExperienceLevel() {
        return experienceLevel;
    }
    
    public void setExperienceLevel(String experienceLevel) {
        this.experienceLevel = experienceLevel;
    }
    
    public String getBio() {
        return bio;
    }
    
    public void setBio(String bio) {
        this.bio = bio;
    }
    
    public String getLocation() {
        return location;
    }
    
    public void setLocation(String location) {
        this.location = location;
    }
    
    public String getGithubProfile() {
        return githubProfile;
    }
    
    public void setGithubProfile(String githubProfile) {
        this.githubProfile = githubProfile;
    }
    
    public Set<Technology> getSkills() {
        return skills;
    }
    
    public void setSkills(Set<Technology> skills) {
        this.skills = skills;
    }
    
    public Set<Experience> getExperiences() {
        return experiences;
    }
    
    public void setExperiences(Set<Experience> experiences) {
        this.experiences = experiences;
    }
    
    // Helper methods
    public void addExperience(Experience experience) {
        experiences.add(experience);
        experience.setDeveloper(this);
    }
    
    public void removeExperience(Experience experience) {
        experiences.remove(experience);
        experience.setDeveloper(null);
    }
    
    @Override
    public String toString() {
        return "Developer{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", experienceLevel='" + experienceLevel + '\'' +
                '}';
    }
}
