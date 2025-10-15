# ============================================================
# DevMatch AI - Migration from SQLite to PostgreSQL
# ============================================================

import os
import sqlite3
from flask import Flask
from models import db, Project, Developer, Technology, Experience
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create Flask app with PostgreSQL configuration"""
    app = Flask(__name__)
    
    # PostgreSQL Configuration
    db_user = os.getenv('DB_USER', 'calebnehemias')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'devmatch_ai')
    
    # Construct DATABASE_URL
    if db_password:
        database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    else:
        database_url = f'postgresql://{db_user}@{db_host}:{db_port}/{db_name}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def migrate_from_sqlite():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Check if SQLite database exists
    sqlite_path = 'instance/devmatch.db'
    if not os.path.exists(sqlite_path):
        print("❌ SQLite database not found at:", sqlite_path)
        return False
    
    print("🔄 Starting migration from SQLite to PostgreSQL...")
    
    # Create PostgreSQL app
    pg_app = create_app()
    
    with pg_app.app_context():
        # Create all tables
        print("📋 Creating PostgreSQL tables...")
        db.create_all()
        
        # Check if data already exists
        if Technology.query.first():
            print("⚠️  PostgreSQL database already contains data!")
            if input("Do you want to continue? This will duplicate data (y/N): ").lower() != 'y':
                return False
        
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row  # Enable column access by name
        
        try:
            # 1. Migrate Technologies
            print("🔧 Migrating technologies...")
            cursor = sqlite_conn.execute("SELECT * FROM technologies")
            tech_mapping = {}
            
            for row in cursor:
                tech = Technology(
                    name=row['name'],
                    category=row['category']
                )
                db.session.add(tech)
                db.session.flush()
                tech_mapping[row['id']] = tech.id
            
            db.session.commit()
            print(f"   ✅ Migrated {len(tech_mapping)} technologies")
            
            # 2. Migrate Projects
            print("📁 Migrating projects...")
            cursor = sqlite_conn.execute("SELECT * FROM projects")
            project_mapping = {}
            
            for row in cursor:
                project = Project(
                    name=row['name'],
                    description=row['description'],
                    experience_level=row['experience_level'],
                    project_type=row['project_type'],
                    status=row['status']
                )
                db.session.add(project)
                db.session.flush()
                project_mapping[row['id']] = project
            
            db.session.commit()
            print(f"   ✅ Migrated {len(project_mapping)} projects")
            
            # 3. Migrate Developers
            print("👥 Migrating developers...")
            cursor = sqlite_conn.execute("SELECT * FROM developers")
            developer_mapping = {}
            
            for row in cursor:
                developer = Developer(
                    name=row['name'],
                    experience_level=row['experience_level'],
                    motivation=row['motivation'],
                    email=row['email'],
                    linkedin=row['linkedin'],
                    github=row['github']
                )
                db.session.add(developer)
                db.session.flush()
                developer_mapping[row['id']] = developer
            
            db.session.commit()
            print(f"   ✅ Migrated {len(developer_mapping)} developers")
            
            # 4. Migrate Project Technologies (many-to-many)
            print("🔗 Migrating project-technology relationships...")
            cursor = sqlite_conn.execute("SELECT * FROM project_technologies")
            
            for row in cursor:
                if row['project_id'] in project_mapping and row['technology_id'] in tech_mapping:
                    project = project_mapping[row['project_id']]
                    tech = Technology.query.get(tech_mapping[row['technology_id']])
                    if tech:
                        project.required_technologies.append(tech)
            
            db.session.commit()
            
            # 5. Migrate Developer Skills (many-to-many)
            print("🛠️  Migrating developer-skill relationships...")
            cursor = sqlite_conn.execute("SELECT * FROM developer_skills")
            
            for row in cursor:
                if row['developer_id'] in developer_mapping and row['technology_id'] in tech_mapping:
                    developer = developer_mapping[row['developer_id']]
                    tech = Technology.query.get(tech_mapping[row['technology_id']])
                    if tech:
                        developer.skills.append(tech)
            
            db.session.commit()
            
            # 6. Migrate Experiences
            print("📋 Migrating experiences...")
            cursor = sqlite_conn.execute("SELECT * FROM experiences")
            
            for row in cursor:
                if row['developer_id'] in developer_mapping:
                    developer = developer_mapping[row['developer_id']]
                    experience = Experience(
                        developer_id=developer.id,
                        description=row['description'],
                        category=row['category']
                    )
                    db.session.add(experience)
            
            db.session.commit()
            
            # Final statistics
            print("\n🎉 Migration completed successfully!")
            print(f"📊 Final counts:")
            print(f"   Technologies: {Technology.query.count()}")
            print(f"   Projects: {Project.query.count()}")
            print(f"   Developers: {Developer.query.count()}")
            print(f"   Experiences: {Experience.query.count()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Migration error: {e}")
            db.session.rollback()
            return False
            
        finally:
            sqlite_conn.close()

if __name__ == "__main__":
    print("🚀 DevMatch AI - SQLite to PostgreSQL Migration")
    print("=" * 50)
    
    if migrate_from_sqlite():
        print("\n✅ Migration successful!")
        print("🔧 You can now use pgAdmin to view your data:")
        print("   1. Open pgAdmin 4 application")
        print("   2. Create new server connection:")
        print("      - Host: localhost")
        print("      - Port: 5432") 
        print("      - Database: devmatch_ai")
        print(f"      - Username: {os.getenv('DB_USER', 'calebnehemias')}")
        print("      - Password: (leave empty if no password)")
        print("\n🌐 Web interface will be available at: http://localhost:3000")
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above.")