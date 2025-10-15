# ============================================================
# DevMatch AI - Flask Web Server
# ============================================================

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Developer, Technology, Experience, Project
from database import (get_all_projects, get_all_developers, 
                     get_project_by_id, get_developer_by_id, calculate_match_db)
from modelai3 import analyze_with_deepseek
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# PostgreSQL Database configuration
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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize database
db.init_app(app)

# Register API Blueprint (CRUD REST endpoints)
from api_routes import api_bp
app.register_blueprint(api_bp)

@app.route('/')
def index():
    """Main route - Homepage with system overview"""
    projects = get_all_projects()
    developers = get_all_developers()
    return render_template('index.html', projects=projects, developers=developers)

@app.route('/projects')
def projects():
    """Projects listing page"""
    projects_list = get_all_projects()
    return render_template('projects.html', projects=projects_list)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """Create a new project"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            experience_level = request.form.get('experience_level', '')
            project_type = request.form.get('project_type', '')
            status = request.form.get('status', 'Open')
            
            # Get selected technologies
            selected_technologies = request.form.getlist('technologies')
            
            # Validation
            if not name:
                flash('El nombre del proyecto es requerido', 'error')
                return redirect(url_for('new_project'))
            
            if not description:
                flash('La descripción del proyecto es requerida', 'error')
                return redirect(url_for('new_project'))
            
            if not experience_level:
                flash('El nivel de experiencia es requerido', 'error')
                return redirect(url_for('new_project'))
            
            if not project_type:
                flash('El tipo de proyecto es requerido', 'error')
                return redirect(url_for('new_project'))
            
            # Create new project
            project = Project(
                name=name,
                description=description,
                experience_level=experience_level,
                project_type=project_type,
                status=status
            )
            
            # Add required technologies
            for tech_id in selected_technologies:
                technology = Technology.query.get(int(tech_id))
                if technology:
                    project.required_technologies.append(technology)
            
            db.session.add(project)
            db.session.commit()
            
            flash(f'Proyecto {name} creado exitosamente!', 'success')
            return redirect(url_for('project_detail', project_id=project.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el proyecto: {str(e)}', 'error')
            return redirect(url_for('new_project'))
    
    # GET request - show form
    technologies = Technology.query.order_by(Technology.name).all()
    return render_template('project_form.html', 
                         project=None, 
                         technologies=technologies,
                         action='create')

@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    """Edit an existing project"""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            experience_level = request.form.get('experience_level', '')
            project_type = request.form.get('project_type', '')
            status = request.form.get('status', 'Open')
            
            # Get selected technologies
            selected_technologies = request.form.getlist('technologies')
            
            # Validation
            if not name:
                flash('El nombre del proyecto es requerido', 'error')
                return redirect(url_for('edit_project', project_id=project_id))
            
            if not description:
                flash('La descripción del proyecto es requerida', 'error')
                return redirect(url_for('edit_project', project_id=project_id))
            
            if not experience_level:
                flash('El nivel de experiencia es requerido', 'error')
                return redirect(url_for('edit_project', project_id=project_id))
            
            if not project_type:
                flash('El tipo de proyecto es requerido', 'error')
                return redirect(url_for('edit_project', project_id=project_id))
            
            # Update project data
            project.name = name
            project.description = description
            project.experience_level = experience_level
            project.project_type = project_type
            project.status = status
            
            # Update technologies - clear and re-add
            project.required_technologies.clear()
            for tech_id in selected_technologies:
                technology = Technology.query.get(int(tech_id))
                if technology:
                    project.required_technologies.append(technology)
            
            db.session.commit()
            
            flash(f'Proyecto {name} actualizado exitosamente!', 'success')
            return redirect(url_for('project_detail', project_id=project.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el proyecto: {str(e)}', 'error')
            return redirect(url_for('edit_project', project_id=project_id))
    
    # GET request - show form with current data
    technologies = Technology.query.order_by(Technology.name).all()
    return render_template('project_form.html', 
                         project=project, 
                         technologies=technologies,
                         action='edit')

@app.route('/projects/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    """Delete a project"""
    project = Project.query.get_or_404(project_id)
    
    try:
        project_name = project.name
        db.session.delete(project)
        db.session.commit()
        flash(f'Proyecto {project_name} eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el proyecto: {str(e)}', 'error')
    
    return redirect(url_for('projects'))

@app.route('/developers')
def developers():
    """Developers listing page"""
    developers_list = get_all_developers()
    return render_template('developers.html', developers=developers_list)

@app.route('/developers/new', methods=['GET', 'POST'])
def new_developer():
    """Create a new developer"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            experience_level = request.form.get('experience_level', '')
            motivation = request.form.get('motivation', '').strip()
            email = request.form.get('email', '').strip()
            linkedin = request.form.get('linkedin', '').strip()
            github = request.form.get('github', '').strip()
            
            # Get selected skills
            selected_skills = request.form.getlist('skills')
            
            # Get experiences (from dynamic form)
            experiences_data = []
            exp_descriptions = request.form.getlist('experience_description[]')
            exp_categories = request.form.getlist('experience_category[]')
            
            for i in range(len(exp_descriptions)):
                if exp_descriptions[i].strip():
                    experiences_data.append({
                        'description': exp_descriptions[i].strip(),
                        'category': exp_categories[i] if i < len(exp_categories) else 'project'
                    })
            
            # Validation
            if not name:
                flash('El nombre es requerido', 'error')
                return redirect(url_for('new_developer'))
            
            if not experience_level:
                flash('El nivel de experiencia es requerido', 'error')
                return redirect(url_for('new_developer'))
            
            # Create new developer
            developer = Developer(
                name=name,
                experience_level=experience_level,
                motivation=motivation,
                email=email if email else None,
                linkedin=linkedin if linkedin else None,
                github=github if github else None
            )
            
            # Add skills
            for skill_id in selected_skills:
                skill = Technology.query.get(int(skill_id))
                if skill:
                    developer.skills.append(skill)
            
            # Save developer first
            db.session.add(developer)
            db.session.flush()  # Get the ID
            
            # Add experiences
            for exp_data in experiences_data:
                experience = Experience(
                    developer_id=developer.id,
                    description=exp_data['description'],
                    category=exp_data['category']
                )
                db.session.add(experience)
            
            db.session.commit()
            flash(f'Desarrollador {name} creado exitosamente!', 'success')
            return redirect(url_for('developer_detail', developer_id=developer.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el desarrollador: {str(e)}', 'error')
            return redirect(url_for('new_developer'))
    
    # GET request - show form
    technologies = Technology.query.order_by(Technology.name).all()
    return render_template('developer_form.html', 
                         developer=None, 
                         technologies=technologies,
                         action='create')

@app.route('/developers/<int:developer_id>/edit', methods=['GET', 'POST'])
def edit_developer(developer_id):
    """Edit an existing developer"""
    developer = Developer.query.get_or_404(developer_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            experience_level = request.form.get('experience_level', '')
            motivation = request.form.get('motivation', '').strip()
            email = request.form.get('email', '').strip()
            linkedin = request.form.get('linkedin', '').strip()
            github = request.form.get('github', '').strip()
            
            # Get selected skills
            selected_skills = request.form.getlist('skills')
            
            # Get experiences
            experiences_data = []
            exp_descriptions = request.form.getlist('experience_description[]')
            exp_categories = request.form.getlist('experience_category[]')
            
            for i in range(len(exp_descriptions)):
                if exp_descriptions[i].strip():
                    experiences_data.append({
                        'description': exp_descriptions[i].strip(),
                        'category': exp_categories[i] if i < len(exp_categories) else 'project'
                    })
            
            # Validation
            if not name:
                flash('El nombre es requerido', 'error')
                return redirect(url_for('edit_developer', developer_id=developer_id))
            
            if not experience_level:
                flash('El nivel de experiencia es requerido', 'error')
                return redirect(url_for('edit_developer', developer_id=developer_id))
            
            # Update developer data
            developer.name = name
            developer.experience_level = experience_level
            developer.motivation = motivation
            developer.email = email if email else None
            developer.linkedin = linkedin if linkedin else None
            developer.github = github if github else None
            
            # Update skills - clear and re-add
            developer.skills.clear()
            for skill_id in selected_skills:
                skill = Technology.query.get(int(skill_id))
                if skill:
                    developer.skills.append(skill)
            
            # Update experiences - clear and re-add
            Experience.query.filter_by(developer_id=developer.id).delete()
            for exp_data in experiences_data:
                experience = Experience(
                    developer_id=developer.id,
                    description=exp_data['description'],
                    category=exp_data['category']
                )
                db.session.add(experience)
            
            db.session.commit()
            flash(f'Desarrollador {name} actualizado exitosamente!', 'success')
            return redirect(url_for('developer_detail', developer_id=developer.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el desarrollador: {str(e)}', 'error')
            return redirect(url_for('edit_developer', developer_id=developer_id))
    
    # GET request - show form with current data
    technologies = Technology.query.order_by(Technology.name).all()
    return render_template('developer_form.html', 
                         developer=developer, 
                         technologies=technologies,
                         action='edit')

@app.route('/developers/<int:developer_id>/delete', methods=['POST'])
def delete_developer(developer_id):
    """Delete a developer"""
    developer = Developer.query.get_or_404(developer_id)
    
    try:
        developer_name = developer.name
        db.session.delete(developer)
        db.session.commit()
        flash(f'Desarrollador {developer_name} eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el desarrollador: {str(e)}', 'error')
    
    return redirect(url_for('developers'))

@app.route('/matching')
def matching():
    """Matching page where users can select project and find candidates"""
    project_id = request.args.get('project_id', type=int)
    selected_project = None
    results = []
    
    projects_list = get_all_projects()
    
    if project_id:
        selected_project = get_project_by_id(project_id)
        if selected_project:
            # Perform matching analysis
            developers_list = get_all_developers()
            for dev in developers_list:
                technical_match = calculate_match_db(selected_project, dev)
                ai_analysis = analyze_with_deepseek(selected_project, dev)
                
                results.append({
                    "developer": dev,
                    "technical_match": technical_match,
                    "ai_analysis": ai_analysis
                })
            
            # Sort by average score (descending)
            results.sort(key=lambda x: (
                x["technical_match"] + 
                x["ai_analysis"].get("technical_affinity", 0) + 
                x["ai_analysis"].get("motivational_affinity", 0) + 
                x["ai_analysis"].get("experience_relevance", 0)
            ) / 4, reverse=True)
    
    return render_template('matching.html', 
                         projects=projects_list, 
                         selected_project=selected_project, 
                         results=results)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Show detailed information for a specific project"""
    project = get_project_by_id(project_id)
    if not project:
        return "Project not found", 404
    
    # Generate matches for this project
    matches = []
    developers_list = get_all_developers()
    for dev in developers_list:
        technical_match = calculate_match_db(project, dev)
        ai_analysis = analyze_with_deepseek(project, dev)
        
        matches.append({
            "developer": dev,
            "technical_match": technical_match,
            "ai_analysis": ai_analysis
        })
    
    # Sort matches by average score
    matches.sort(key=lambda x: (
        x["technical_match"] + 
        x["ai_analysis"].get("technical_affinity", 0) + 
        x["ai_analysis"].get("motivational_affinity", 0) + 
        x["ai_analysis"].get("experience_relevance", 0)
    ) / 4, reverse=True)
    
    return render_template('project_detail.html', project=project, matches=matches)

@app.route('/developer/<int:developer_id>')
def developer_detail(developer_id):
    """Show detailed information for a specific developer"""
    developer = get_developer_by_id(developer_id)
    if not developer:
        return "Developer not found", 404
    
    projects_list = get_all_projects()
    return render_template('developer_detail.html', 
                         developer=developer, 
                         projects=projects_list, 
                         calculate_match=calculate_match_db)

@app.route('/api/results')
def api_results():
    """API endpoint that returns JSON results"""
    results = []
    
    projects_list = get_all_projects()
    developers_list = get_all_developers()
    
    for project in projects_list:
        project_results = {
            "project": project,
            "matches": []
        }
        
        for dev in developers_list:
            score = calculate_match_db(project, dev)
            analysis = analyze_with_deepseek(project, dev)
            
            match_data = {
                "developer": dev,
                "technical_match": score,
                "ai_analysis": analysis
            }
            project_results["matches"].append(match_data)
        
        results.append(project_results)
    
    return jsonify({"results": results})

if __name__ == '__main__':
    print("🚀 Starting DevMatch AI Flask Server...")
    print("📱 Access the web interface at: http://localhost:3000")
    print("📊 Available pages:")
    print("   🏠 Homepage: http://localhost:3000")
    print("   🗂️  Projects: http://localhost:3000/projects")
    print("   👥 Developers: http://localhost:3000/developers")
    print("   🔍 Find Match: http://localhost:3000/matching")
    print("   📊 API: http://localhost:3000/api/results")
    print("\n✨ Features:")
    print("   - AI-powered matching with DeepSeek")
    print("   - Interactive project-developer matching")
    print("   - Detailed profiles and compatibility analysis")
    print("   - Responsive web design")
    
    # Usar puerto 3000 para Docker y detectar si estamos en producción
    port = int(os.getenv('PORT', 3000))
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)