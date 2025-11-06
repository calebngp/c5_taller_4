# ============================================================
# Script para eliminar proyectos por nombre
# ============================================================

import os
from flask import Flask
from models import db, Project, MatchResult
from dotenv import load_dotenv

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

def delete_project_by_name(project_name):
    """Elimina un proyecto por su nombre (o todos los que coincidan)"""
    app = create_app()
    
    with app.app_context():
        # Buscar proyectos por nombre (case insensitive)
        projects = Project.query.filter(Project.name.ilike(f'%{project_name}%')).all()
        
        if not projects:
            print(f"❌ No se encontraron proyectos con el nombre '{project_name}'")
            return
        
        print(f"🔍 Encontrados {len(projects)} proyecto(s) con el nombre '{project_name}':")
        for project in projects:
            print(f"   - ID: {project.id}, Nombre: {project.name}")
        
        # Confirmar eliminación
        confirm = input(f"\n¿Deseas eliminar estos {len(projects)} proyecto(s)? (s/n): ").lower()
        
        if confirm != 's':
            print("❌ Operación cancelada")
            return
        
        # Eliminar matches asociados primero
        deleted_matches = 0
        for project in projects:
            matches = MatchResult.query.filter_by(project_id=project.id).all()
            for match in matches:
                db.session.delete(match)
                deleted_matches += 1
        
        # Eliminar proyectos
        deleted_projects = []
        for project in projects:
            project_name_deleted = project.name
            db.session.delete(project)
            deleted_projects.append(project_name_deleted)
        
        db.session.commit()
        
        print(f"\n✅ Eliminación completada:")
        print(f"   - {len(deleted_projects)} proyecto(s) eliminado(s)")
        print(f"   - {deleted_matches} match(es) eliminado(s)")
        print(f"\n📋 Proyectos eliminados:")
        for name in deleted_projects:
            print(f"   - {name}")

def list_all_projects():
    """Lista todos los proyectos en la base de datos"""
    app = create_app()
    
    with app.app_context():
        projects = Project.query.order_by(Project.name).all()
        
        if not projects:
            print("❌ No hay proyectos en la base de datos")
            return
        
        print(f"\n📋 Proyectos en la base de datos ({len(projects)} total):\n")
        for project in projects:
            match_count = MatchResult.query.filter_by(project_id=project.id).count()
            print(f"   ID: {project.id:3d} | Nombre: {project.name:50s} | Matches: {match_count:3d}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list' or sys.argv[1] == '-l':
            list_all_projects()
        else:
            project_name = sys.argv[1]
            delete_project_by_name(project_name)
    else:
        print("Uso:")
        print("  python delete_project.py 'Nombre del Proyecto'  - Elimina proyectos por nombre")
        print("  python delete_project.py --list                 - Lista todos los proyectos")
        print("\nEjemplo:")
        print("  python delete_project.py 'Taller IV'")
