# ============================================================
# DevMatch AI - Integrated with DeepSeek for semantic analysis
# ============================================================

import json
import subprocess
from typing import Dict

# -------------------------------
# Pre-loaded data
# -------------------------------

projects = [
    {
        "id": 1,
        "name": "Coffee shop ordering system",
        "description": "Web application to manage orders, menus and deliveries in coffee shops. We're looking for people who enjoy collaborative work and improving customer experience.",
        "required_technologies": ["Java", "Spring Boot", "PostgreSQL", "HTML", "CSS"],
        "experience_level": "Intermediate",
        "project_type": "Web",
        "status": "Open"
    },
    {
        "id": 2,
        "name": "Fitness mobile app with progress tracking",
        "description": "Mobile application to record workout routines, motivate users and offer health recommendations based on data.",
        "required_technologies": ["Kotlin", "Firebase", "UI/UX"],
        "experience_level": "Advanced",
        "project_type": "Mobile",
        "status": "Open"
    },
    {
        "id": 3,
        "name": "Online course platform with integrated payments",
        "description": "Website for teaching video courses, with user management, payment system and progress analysis.",
        "required_technologies": ["Python", "Django", "Stripe API", "JavaScript"],
        "experience_level": "Intermediate",
        "project_type": "Web",
        "status": "Open"
    }
]

developers = [
    {
        "id": 1,
        "name": "Ana López",
        "skills": ["Java", "Spring Boot", "PostgreSQL", "HTML"],
        "experience_level": "Intermediate",
        "motivation": "I like working on projects where I can impact user experience. I'm interested in growing in web software architecture.",
        "experiences": [
            "Worked as a barista at a local coffee shop while studying systems analysis - understood customer flow and order management challenges",
            "Built a small inventory system for my uncle's restaurant using Java",
            "Participated in a hackathon focused on improving retail customer experience"
        ]
    },
    {
        "id": 2,
        "name": "Carlos Pérez",
        "skills": ["Kotlin", "Firebase", "UI/UX", "Java"],
        "experience_level": "Advanced",
        "motivation": "Passionate about mobile apps and interface optimization. I look for challenges involving design and performance.",
        "experiences": [
            "Personal trainer for 3 years while learning programming - deep understanding of fitness routines and user motivation",
            "Created a workout tracking app for personal use that got 500+ downloads",
            "Worked at a gym doing membership management and saw the need for better digital tools",
            "Studied sports science before switching to computer science"
        ]
    },
    {
        "id": 3,
        "name": "Lucía Martínez",
        "skills": ["Python", "Django", "JavaScript", "React", "Stripe API"],
        "experience_level": "Intermediate",
        "motivation": "I enjoy teaching and learning. I love working on educational or social impact projects.",
        "experiences": [
            "Worked as a private math tutor for 4 years - understand learning processes and student engagement",
            "Organized coding workshops at community centers",
            "Built a small e-commerce site for a friend's art business using Django and Stripe",
            "Volunteered teaching basic computer skills to seniors",
            "Created educational content for a local coding bootcamp"
        ]
    }
]

# -------------------------------
# Technical matching function
# -------------------------------

def calculate_match(project: Dict, developer: Dict) -> float:
    required = set(project["required_technologies"])
    skills = set(developer["skills"])
    matches = required & skills
    if not required:
        return 0
    return (len(matches) / len(required)) * 100


# -------------------------------
# DeepSeek integration (Ollama)
# -------------------------------

def analyze_with_deepseek(project: Dict, developer: Dict) -> str:
    """Sends description and profile to DeepSeek for semantic analysis."""
    experiences_text = "\n".join([f"- {exp}" for exp in developer["experiences"]])
    
    prompt = f"""
You are an intelligent matching assistant.
Analyze if the following developer fits this project and explain why.

Project:
Name: {project['name']}
Description: {project['description']}
Required technologies: {', '.join(project['required_technologies'])}

Developer:
Name: {developer['name']}
Skills: {', '.join(developer['skills'])}
Experience level: {developer['experience_level']}
Motivation: {developer['motivation']}

Previous Experiences:
{experiences_text}

Evaluate technical affinity and motivational affinity (0 to 100) considering both skills and relevant experiences.
Pay special attention to how past experiences might relate to the project domain, even if indirectly.
Respond in JSON format:
{{"technical_affinity": X, "motivational_affinity": Y, "experience_relevance": Z, "comment": "brief explanation"}}
"""
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:1.5b"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode("utf-8").strip()

    # Try to parse JSON from model
    try:
        start = output.find("{")
        end = output.rfind("}") + 1
        parsed = json.loads(output[start:end])
        return parsed
    except Exception:
        return {"technical_affinity": 0, "motivational_affinity": 0, "experience_relevance": 0, "comment": output}


# -------------------------------
# Show results
# -------------------------------

def show_results():
    print("\n=== MATCHING RESULTS WITH DEEPSEEK ===\n")
    for project in projects:
        print(f"\nProject: {project['name']}")
        print(f"Description: {project['description']}")
        print("------------------------------------------------")
        for dev in developers:
            score = calculate_match(project, dev)
            analysis = analyze_with_deepseek(project, dev)
            print(f"👤 {dev['name']}")
            print(f"  ▸ Technical match: {score:.1f}%")
            print(f"  ▸ Technical affinity (AI): {analysis['technical_affinity']}%")
            print(f"  ▸ Motivational affinity (AI): {analysis['motivational_affinity']}%")
            print(f"  ▸ Experience relevance (AI): {analysis['experience_relevance']}%")
            print(f"  💬 {analysis['comment']}")
            print("  📋 Relevant experiences:")
            for exp in dev['experiences']:
                print(f"     • {exp}")
            print("------------------------------------------------")


# -------------------------------
# Execution
# -------------------------------

if __name__ == "__main__":
    show_results()
