# ============================================================
# DevMatch AI - Database Administration CLI
# ============================================================

import click
from flask import Flask
from models import db, Project, Developer, Technology, Experience
from database import init_database, get_all_projects, get_all_developers

def create_app():
    """Create Flask app for CLI operations"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devmatch.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

@click.group()
def cli():
    """DevMatch AI Database Administration"""
    pass

@cli.command()
def init():
    """Initialize database with sample data"""
    app = create_app()
    with app.app_context():
        init_database(app)
        click.echo("✅ Database initialized successfully!")

@cli.command()
def stats():
    """Show database statistics"""
    app = create_app()
    with app.app_context():
        projects_count = Project.query.count()
        developers_count = Developer.query.count()
        technologies_count = Technology.query.count()
        experiences_count = Experience.query.count()
        
        click.echo(f"📊 Database Statistics:")
        click.echo(f"   Projects: {projects_count}")
        click.echo(f"   Developers: {developers_count}")
        click.echo(f"   Technologies: {technologies_count}")
        click.echo(f"   Experiences: {experiences_count}")

@cli.command()
def reset():
    """Reset database (DELETE ALL DATA)"""
    if click.confirm('⚠️  This will delete all data. Are you sure?'):
        app = create_app()
        with app.app_context():
            db.drop_all()
            click.echo("🗑️  Database cleared!")
            init_database(app)
            click.echo("✅ Database reset with sample data!")

@cli.command()
def list_projects():
    """List all projects"""
    app = create_app()
    with app.app_context():
        projects = get_all_projects()
        click.echo(f"📋 Found {len(projects)} projects:")
        for project in projects:
            click.echo(f"   {project['id']}. {project['name']} ({project['project_type']})")

@cli.command()
def list_developers():
    """List all developers"""
    app = create_app()
    with app.app_context():
        developers = get_all_developers()
        click.echo(f"👥 Found {len(developers)} developers:")
        for dev in developers:
            click.echo(f"   {dev['id']}. {dev['name']} ({dev['experience_level']})")

@cli.command()
@click.argument('name')
@click.argument('description')
@click.option('--type', default='Web', help='Project type (Web, Mobile, Desktop)')
@click.option('--level', default='Intermediate', help='Experience level (Beginner, Intermediate, Advanced)')
def add_project(name, description, type, level):
    """Add a new project"""
    app = create_app()
    with app.app_context():
        project = Project(
            name=name,
            description=description,
            project_type=type,
            experience_level=level,
            status='Open'
        )
        db.session.add(project)
        db.session.commit()
        click.echo(f"✅ Added project: {name}")

@cli.command()
@click.argument('name')
@click.option('--level', default='Intermediate', help='Experience level')
@click.option('--motivation', default='', help='Developer motivation')
def add_developer(name, level, motivation):
    """Add a new developer"""
    app = create_app()
    with app.app_context():
        developer = Developer(
            name=name,
            experience_level=level,
            motivation=motivation
        )
        db.session.add(developer)
        db.session.commit()
        click.echo(f"✅ Added developer: {name}")

@cli.command()
@click.argument('tech_name')
@click.option('--category', default='other', help='Technology category')
def add_technology(tech_name, category):
    """Add a new technology"""
    app = create_app()
    with app.app_context():
        # Check if technology already exists
        existing = Technology.query.filter_by(name=tech_name).first()
        if existing:
            click.echo(f"⚠️  Technology '{tech_name}' already exists!")
            return
        
        technology = Technology(
            name=tech_name,
            category=category
        )
        db.session.add(technology)
        db.session.commit()
        click.echo(f"✅ Added technology: {tech_name} ({category})")

@cli.command()
def backup():
    """Create a backup of the database"""
    import shutil
    import datetime
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"devmatch_backup_{timestamp}.db"
    
    try:
        shutil.copy2('devmatch.db', backup_file)
        click.echo(f"✅ Backup created: {backup_file}")
    except FileNotFoundError:
        click.echo("❌ Database file not found!")
    except Exception as e:
        click.echo(f"❌ Backup failed: {e}")

if __name__ == '__main__':
    cli()