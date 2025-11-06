# ============================================================
# DevMatch AI - Database Initialization and Data Migration
# ============================================================

from models import db, Project, Developer, Technology, Experience, MatchResult, AuditHistory
from initial_data import projects as old_projects, developers as old_developers
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

def save_match_result(project_id, developer_id, technical_match, ai_analysis):
    """Save match result to database"""
    try:
        # Check if a match result already exists for this project-developer pair
        existing = MatchResult.query.filter_by(
            project_id=project_id,
            developer_id=developer_id
        ).first()
        
        if existing:
            # Update existing result
            existing.technical_match = technical_match
            existing.ai_technical_affinity = ai_analysis.get('technical_affinity', 0)
            existing.ai_motivational_affinity = ai_analysis.get('motivational_affinity', 0)
            existing.ai_experience_relevance = ai_analysis.get('experience_relevance', 0)
            existing.ai_comment = ai_analysis.get('comment', '')
            existing.created_at = datetime.now().isoformat()
        else:
            # Create new result
            match_result = MatchResult(
                project_id=project_id,
                developer_id=developer_id,
                technical_match=technical_match,
                ai_technical_affinity=ai_analysis.get('technical_affinity', 0),
                ai_motivational_affinity=ai_analysis.get('motivational_affinity', 0),
                ai_experience_relevance=ai_analysis.get('experience_relevance', 0),
                ai_comment=ai_analysis.get('comment', ''),
                created_at=datetime.now().isoformat()
            )
            db.session.add(match_result)
        
        db.session.commit()
        print(f"✅ Match result saved: Project {project_id} - Developer {developer_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving match result: {e}")
        db.session.rollback()
        return False

def get_match_results():
    """Get all match results from database"""
    try:
        results = MatchResult.query.all()
        return [result.to_dict() for result in results]
    except Exception as e:
        print(f"❌ Error getting match results: {e}")
        return []

def get_match_results_for_project(project_id):
    """Get match results for a specific project"""
    try:
        results = MatchResult.query.filter_by(project_id=project_id).all()
        return [result.to_dict() for result in results]
    except Exception as e:
        print(f"❌ Error getting match results for project {project_id}: {e}")
        return []

def get_match_results_for_developer(developer_id):
    """Get match results for a specific developer"""
    try:
        results = MatchResult.query.filter_by(developer_id=developer_id).all()
        return [result.to_dict() for result in results]
    except Exception as e:
        print(f"❌ Error getting match results for developer {developer_id}: {e}")
        return []

def clear_old_match_results():
    """Clear all match results (useful for regenerating results)"""
    try:
        MatchResult.query.delete()
        db.session.commit()
        print("✅ All match results cleared")
        return True
    except Exception as e:
        print(f"❌ Error clearing match results: {e}")
        db.session.rollback()
        return False

def get_match_statistics():
    """Get statistics about saved matches"""
    try:
        total_matches = MatchResult.query.count()
        
        # Best technical matches
        best_technical = MatchResult.query.order_by(MatchResult.technical_match.desc()).limit(3).all()
        
        # Best overall AI scores (average of AI metrics)
        high_ai_scores = db.session.query(MatchResult).all()
        
        stats = {
            'total_matches': total_matches,
            'best_technical_matches': [
                {
                    'project_id': match.project_id,
                    'developer_id': match.developer_id,
                    'technical_match': match.technical_match,
                    'project_name': match.project.name if match.project else 'Unknown',
                    'developer_name': match.developer.name if match.developer else 'Unknown'
                } for match in best_technical
            ],
            'average_technical_score': db.session.query(db.func.avg(MatchResult.technical_match)).scalar() or 0,
            'average_ai_technical': db.session.query(db.func.avg(MatchResult.ai_technical_affinity)).scalar() or 0,
            'average_ai_motivational': db.session.query(db.func.avg(MatchResult.ai_motivational_affinity)).scalar() or 0,
        }
        
        return stats
    except Exception as e:
        print(f"❌ Error getting match statistics: {e}")
        return None

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