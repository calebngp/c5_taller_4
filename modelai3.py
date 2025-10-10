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
# Generate HTML output
# -------------------------------

def generate_html_report():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DevMatch AI - Project-Developer Matching Results</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #2c3e50, #34495e);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .project-section {
                margin: 30px;
                border: 2px solid #e74c3c;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .project-header {
                background: #e74c3c;
                color: white;
                padding: 20px;
            }
            
            .project-title {
                font-size: 1.8em;
                margin-bottom: 10px;
            }
            
            .project-description {
                font-size: 1.1em;
                line-height: 1.5;
                opacity: 0.95;
            }
            
            .project-tech {
                margin-top: 15px;
            }
            
            .tech-tag {
                display: inline-block;
                background: rgba(255,255,255,0.2);
                padding: 5px 12px;
                border-radius: 20px;
                margin: 3px;
                font-size: 0.9em;
            }
            
            .developer-card {
                background: #f8f9fa;
                margin: 20px;
                border-radius: 10px;
                overflow: hidden;
                border: 1px solid #dee2e6;
                transition: transform 0.3s ease;
            }
            
            .developer-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            }
            
            .developer-header {
                background: #3498db;
                color: white;
                padding: 20px;
                display: flex;
                align-items: center;
            }
            
            .developer-name {
                font-size: 1.5em;
                margin-left: 10px;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                padding: 20px;
            }
            
            .metric-card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e9ecef;
            }
            
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .metric-label {
                color: #6c757d;
                font-size: 0.9em;
            }
            
            .technical { color: #28a745; }
            .technical-ai { color: #007bff; }
            .motivational { color: #ffc107; }
            .experience { color: #17a2b8; }
            
            .progress-bar {
                width: 100%;
                height: 8px;
                background: #e9ecef;
                border-radius: 4px;
                margin-top: 8px;
                overflow: hidden;
            }
            
            .progress-fill {
                height: 100%;
                transition: width 0.8s ease;
                border-radius: 4px;
            }
            
            .comment-section {
                padding: 20px;
                background: white;
            }
            
            .comment {
                background: #f1f3f4;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #6c757d;
                margin-bottom: 15px;
            }
            
            .experiences-section {
                padding: 20px;
                background: #f8f9fa;
            }
            
            .experiences-title {
                font-size: 1.2em;
                margin-bottom: 15px;
                color: #495057;
            }
            
            .experience-item {
                background: white;
                padding: 12px;
                margin: 8px 0;
                border-radius: 6px;
                border-left: 3px solid #17a2b8;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            .skills-section {
                padding: 20px;
            }
            
            .skill-tag {
                display: inline-block;
                background: #e9ecef;
                padding: 6px 12px;
                border-radius: 15px;
                margin: 3px;
                font-size: 0.85em;
                color: #495057;
            }
            
            @media (max-width: 768px) {
                .metrics-grid {
                    grid-template-columns: 1fr;
                }
                
                .container {
                    margin: 10px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 DevMatch AI</h1>
                <p>Project-Developer Matching Results with DeepSeek Analysis</p>
            </div>
    """
    
    for project in projects:
        html_content += f"""
            <div class="project-section">
                <div class="project-header">
                    <div class="project-title">🚀 {project['name']}</div>
                    <div class="project-description">{project['description']}</div>
                    <div class="project-tech">
                        <strong>Required Technologies:</strong>
        """
        
        for tech in project['required_technologies']:
            html_content += f'<span class="tech-tag">{tech}</span>'
        
        html_content += f"""
                    </div>
                </div>
        """
        
        for dev in developers:
            score = calculate_match(project, dev)
            analysis = analyze_with_deepseek(project, dev)
            
            html_content += f"""
                <div class="developer-card">
                    <div class="developer-header">
                        <div>👤</div>
                        <div class="developer-name">{dev['name']}</div>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value technical">{score:.1f}%</div>
                            <div class="metric-label">Technical Match</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {score}%; background: #28a745;"></div>
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-value technical-ai">{analysis.get('technical_affinity', 0)}%</div>
                            <div class="metric-label">AI Technical Affinity</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {analysis.get('technical_affinity', 0)}%; background: #007bff;"></div>
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-value motivational">{analysis.get('motivational_affinity', 0)}%</div>
                            <div class="metric-label">Motivational Affinity</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {analysis.get('motivational_affinity', 0)}%; background: #ffc107;"></div>
                            </div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-value experience">{analysis.get('experience_relevance', 0)}%</div>
                            <div class="metric-label">Experience Relevance</div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {analysis.get('experience_relevance', 0)}%; background: #17a2b8;"></div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="comment-section">
                        <div class="comment">
                            <strong>💬 AI Analysis:</strong> {analysis.get('comment', 'No comment available')}
                        </div>
                    </div>
                    
                    <div class="skills-section">
                        <strong>🛠️ Skills:</strong><br>
            """
            
            for skill in dev['skills']:
                html_content += f'<span class="skill-tag">{skill}</span>'
            
            html_content += f"""
                    </div>
                    
                    <div class="experiences-section">
                        <div class="experiences-title">📋 Relevant Experiences:</div>
            """
            
            for exp in dev['experiences']:
                html_content += f'<div class="experience-item">• {exp}</div>'
            
            html_content += """
                    </div>
                </div>
            """
        
        html_content += "</div>"
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    return html_content

def show_results():
    print("\n=== GENERATING HTML REPORT ===\n")
    
    html_content = generate_html_report()
    
    # Save to HTML file
    with open('devmatch_results.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML report generated successfully!")
    print("📄 File saved as: devmatch_results.html")
    print("🌐 Open the file in your web browser to view the results")
    
    # Also print console results
    print("\n=== CONSOLE RESULTS ===\n")
    for project in projects:
        print(f"\nProject: {project['name']}")
        print(f"Description: {project['description']}")
        print("------------------------------------------------")
        for dev in developers:
            score = calculate_match(project, dev)
            analysis = analyze_with_deepseek(project, dev)
            print(f"👤 {dev['name']}")
            print(f"  ▸ Technical match: {score:.1f}%")
            print(f"  ▸ Technical affinity (AI): {analysis.get('technical_affinity', 0)}%")
            print(f"  ▸ Motivational affinity (AI): {analysis.get('motivational_affinity', 0)}%")
            print(f"  ▸ Experience relevance (AI): {analysis.get('experience_relevance', 0)}%")
            print(f"  💬 {analysis.get('comment', 'No comment available')}")
            print("  📋 Relevant experiences:")
            for exp in dev['experiences']:
                print(f"     • {exp}")
            print("------------------------------------------------")


# -------------------------------
# Execution
# -------------------------------

if __name__ == "__main__":
    show_results()
