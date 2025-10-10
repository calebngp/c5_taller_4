# ============================================================
# DevMatch AI - Database Initialization and Data Migration
# ============================================================

from models import db, Project, Developer, Technology, Experience
from modelai3 import projects as old_projects, developers as old_developers
from datetime import datetime
import os

def init_database(app):
    """Initialize the database with tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if data already exists
        if Technology.query.first():
            print("ℹ️  Database already contains data. Skipping migration.")
            return
        
        # Migrate data
        migrate_data()
        print("🚀 Data migration completed successfully!")

def migrate_data():
    """Migrate data from modelai3.py to the database"""
    
    # 1. Create Technologies
    print("📊 Migrating technologies...")
    tech_mapping = {}
    
    # Collect all unique technologies
    all_techs = set()
    for project in old_projects:
        all_techs.update(project["required_technologies"])
    for developer in old_developers:
        all_techs.update(developer["skills"])
    
    # Create technology records with categories
    tech_categories = {
        # Backend
        'Java': 'backend',
        'Spring Boot': 'backend', 
        'Python': 'backend',
        'Django': 'backend',
        'PostgreSQL': 'database',
        
        # Frontend
        'HTML': 'frontend',
        'CSS': 'frontend', 
        'JavaScript': 'frontend',
        'React': 'frontend',
        'UI/UX': 'design',
        
        # Mobile
        'Kotlin': 'mobile',
        'Firebase': 'backend',
        
        # APIs
        'Stripe API': 'api'
    }
    
    for tech_name in sorted(all_techs):
        tech = Technology(
            name=tech_name,
            category=tech_categories.get(tech_name, 'other')
        )
        db.session.add(tech)
        db.session.flush()  # Get the ID
        tech_mapping[tech_name] = tech
    
    db.session.commit()
    print(f"   ✅ Created {len(tech_mapping)} technologies")
    
    # 2. Create Projects
    print("🗂️  Migrating projects...")
    for old_project in old_projects:
        project = Project(
            name=old_project["name"],
            description=old_project["description"],
            experience_level=old_project["experience_level"],
            project_type=old_project["project_type"],
            status=old_project["status"]
        )
        
        # Add required technologies
        for tech_name in old_project["required_technologies"]:
            if tech_name in tech_mapping:
                project.required_technologies.append(tech_mapping[tech_name])
        
        db.session.add(project)
    
    db.session.commit()
    print(f"   ✅ Created {len(old_projects)} projects")
    
    # 3. Create Developers with Experiences
    print("👥 Migrating developers...")
    for old_dev in old_developers:
        developer = Developer(
            name=old_dev["name"],
            experience_level=old_dev["experience_level"],
            motivation=old_dev["motivation"]
        )
        
        # Add skills
        for skill_name in old_dev["skills"]:
            if skill_name in tech_mapping:
                developer.skills.append(tech_mapping[skill_name])
        
        db.session.add(developer)
        db.session.flush()  # Get the ID
        
        # Add experiences
        for exp_text in old_dev["experiences"]:
            experience = Experience(
                developer_id=developer.id,
                description=exp_text,
                category='work'  # Default category
            )
            db.session.add(experience)
    
    db.session.commit()
    print(f"   ✅ Created {len(old_developers)} developers")

def get_all_projects():
    """Get all projects from database"""
    projects = Project.query.all()
    return [project.to_dict() for project in projects]

def get_all_developers():
    """Get all developers from database"""
    developers = Developer.query.all()
    return [developer.to_dict() for developer in developers]

def get_project_by_id(project_id):
    """Get a specific project by ID"""
    project = Project.query.get(project_id)
    return project.to_dict() if project else None

def get_developer_by_id(developer_id):
    """Get a specific developer by ID"""
    developer = Developer.query.get(developer_id)
    return developer.to_dict() if developer else None

def calculate_match_db(project_dict, developer_dict):
    """Calculate technical match between project and developer (database version)"""
    required = set(project_dict["required_technologies"])
    skills = set(developer_dict["skills"])
    matches = required & skills
    if not required:
        return 0
    return (len(matches) / len(required)) * 100

if __name__ == "__main__":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    # Create Flask app for testing
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devmatch.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Initialize database
    init_database(app)
    
    # Test queries
    with app.app_context():
        projects = get_all_projects()
        developers = get_all_developers()
        
        print(f"\n📊 Database Statistics:")
        print(f"   Projects: {len(projects)}")
        print(f"   Developers: {len(developers)}")
        print(f"   Technologies: {Technology.query.count()}")
        print(f"   Experiences: {Experience.query.count()}")
        
        print(f"\n🎯 Sample Data:")
        if projects:
            print(f"   First project: {projects[0]['name']}")
        if developers:
            print(f"   First developer: {developers[0]['name']}")