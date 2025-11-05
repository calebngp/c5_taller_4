# ============================================================
# DevMatch AI - Flask Web Server
# ============================================================

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from models import db, Developer, Technology, Experience, Project
from database import (get_all_projects, get_all_developers, 
                     get_project_by_id, get_developer_by_id, calculate_match_db,
                     save_match_result, get_match_results_for_project)
from modelai3 import analyze_with_deepseek
from dotenv import load_dotenv
import json
import subprocess

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
            # Get project from database
            project = Project.query.get(project_id)
            if not project:
                flash('Proyecto no encontrado', 'error')
                return redirect(url_for('matching'))
            
            # Perform matching analysis
            developers_list = get_all_developers()
            for dev_dict in developers_list:
                dev = Developer.query.get(dev_dict['id'])
                if not dev:
                    continue
                
                technical_match = calculate_match_db(selected_project, dev_dict)
                ai_analysis = analyze_with_deepseek(selected_project, dev_dict)
                
                # Save match result to database
                save_match_result(project_id, dev.id, technical_match, ai_analysis)
                
                results.append({
                    "developer": dev_dict,
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
    
    # Get project from database
    project_obj = Project.query.get(project_id)
    if not project_obj:
        return "Project not found", 404
    
    # Generate matches for this project
    matches = []
    developers_list = get_all_developers()
    for dev_dict in developers_list:
        dev = Developer.query.get(dev_dict['id'])
        if not dev:
            continue
        
        technical_match = calculate_match_db(project, dev_dict)
        ai_analysis = analyze_with_deepseek(project, dev_dict)
        
        # Save match result to database
        save_match_result(project_id, dev.id, technical_match, ai_analysis)
        
        matches.append({
            "developer": dev_dict,
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

@app.route('/projects/matches')
def projects_with_matches():
    """Show all projects with their saved matches"""
    from models import MatchResult
    
    projects_list = get_all_projects()
    projects_with_matches_data = []
    
    for project_dict in projects_list:
        project = Project.query.get(project_dict['id'])
        if not project:
            continue
        
        # Get saved matches for this project
        saved_matches = MatchResult.query.filter_by(project_id=project.id).order_by(
            MatchResult.technical_match.desc()
        ).all()
        
        matches_data = []
        for match_result in saved_matches:
            developer = Developer.query.get(match_result.developer_id)
            if developer:
                matches_data.append({
                    "match_result": match_result,
                    "developer": developer.to_dict(),
                    "technical_match": match_result.technical_match,
                    "ai_technical_affinity": match_result.ai_technical_affinity,
                    "ai_motivational_affinity": match_result.ai_motivational_affinity,
                    "ai_experience_relevance": match_result.ai_experience_relevance,
                    "ai_comment": match_result.ai_comment,
                    "created_at": match_result.created_at
                })
        
        # Calculate average match score
        avg_score = 0
        if matches_data:
            total = sum([
                m["technical_match"] + 
                (m["ai_technical_affinity"] or 0) + 
                (m["ai_motivational_affinity"] or 0) + 
                (m["ai_experience_relevance"] or 0)
                for m in matches_data
            ])
            avg_score = total / (len(matches_data) * 4) if matches_data else 0
        
        projects_with_matches_data.append({
            "project": project_dict,
            "matches": matches_data,
            "match_count": len(matches_data),
            "average_score": avg_score
        })
    
    # Sort by match count (descending) and then by average score
    projects_with_matches_data.sort(key=lambda x: (x["match_count"], x["average_score"]), reverse=True)
    
    # Calculate statistics
    total_matches = sum(p["match_count"] for p in projects_with_matches_data)
    total_projects = len(projects_with_matches_data)
    avg_matches_per_project = total_matches / total_projects if total_projects > 0 else 0
    avg_score = sum(p["average_score"] for p in projects_with_matches_data) / total_projects if total_projects > 0 else 0
    
    return render_template('projects_matches.html', 
                         projects_with_matches=projects_with_matches_data,
                         total_matches=total_matches,
                         avg_matches_per_project=avg_matches_per_project,
                         avg_score=avg_score)

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

def analyze_project_with_ai(project_description, project_goals="", conversation_history=[]):
    """
    Analiza la descripción del proyecto con IA para sugerir tecnologías, 
    nivel de experiencia, tipo de proyecto y descripción mejorada.
    Mantiene el contexto de la conversación y hace preguntas de seguimiento.
    """
    # Obtener todas las tecnologías disponibles
    technologies = Technology.query.order_by(Technology.name).all()
    tech_names = [tech.name for tech in technologies]
    
    # Limitar la descripción si es muy larga para evitar problemas con el prompt
    max_desc_length = 2000
    if len(project_description) > max_desc_length:
        project_description = project_description[:max_desc_length] + "..."
    
    # Construir el historial de conversación
    history_text = ""
    if conversation_history:
        history_text = "\n\nCONVERSATION HISTORY:\n"
        for msg in conversation_history[-5:]:  # Últimos 5 mensajes para mantener contexto
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            history_text += f"{role.upper()}: {content}\n"
    
    # Determinar si es la primera interacción o hay contexto previo
    is_first_message = len(conversation_history) == 0
    
    if is_first_message:
        # Primera interacción: hacer análisis inicial y preguntas
        prompt = f"""You are an expert software development assistant helping users create well-structured projects. This is the FIRST interaction with the user.

PROJECT DESCRIPTION:
{project_description}

ADDITIONAL GOALS:
{project_goals if project_goals else "None specified"}

AVAILABLE TECHNOLOGIES IN THE SYSTEM (you can only use these):
{', '.join(tech_names)}

Your task:
1. Analyze the project description
2. Provide initial recommendations
3. Ask 2-3 follow-up questions to better understand the project requirements

Respond EXACTLY with this JSON format (no comments, no additional text):
{{
    "name": "Descriptive project name",
    "description": "Professional description based on the provided information",
    "experience_level": "Beginner|Intermediate|Advanced",
    "project_type": "Web|Mobile|Desktop|API|Data Science|DevOps|Other",
    "suggested_technologies": ["name1", "name2"],
    "reasoning": "Brief explanation of why these technologies and experience level are recommended",
    "recommendations": "Detailed recommendations for the project development, including architecture suggestions, best practices, and important considerations",
    "follow_up_questions": [
        "Question 1 to understand the project better",
        "Question 2 about specific requirements",
        "Question 3 about priorities or constraints"
    ],
    "needs_more_info": true
}}

RULES:
- Only use technologies from the provided list
- If you mention a technology not in the list, find the most similar one available
- Analyze the description to determine the required experience level
- The type must be one of: Web, Mobile, Desktop, API, Data Science, DevOps, Other
- Provide DETAILED recommendations (at least 3-4 sentences with specific advice)
- Ask RELEVANT follow-up questions that will help better understand the project
- Respond ONLY with the JSON, without additional text"""
    else:
        # Conversación en curso: usar contexto previo
        prompt = f"""You are an expert software development assistant helping users create well-structured projects. This is a CONTINUATION of the conversation.

CURRENT MESSAGE:
{project_description}

{history_text}

ADDITIONAL GOALS:
{project_goals if project_goals else "None specified"}

AVAILABLE TECHNOLOGIES IN THE SYSTEM (you can only use these):
{', '.join(tech_names)}

Your task:
1. Use the conversation history to understand the full context
2. Update your analysis based on the new information provided
3. Provide comprehensive recommendations
4. If more information is still needed, ask 1-2 follow-up questions. If you have enough information, set needs_more_info to false

Respond EXACTLY with this JSON format (no comments, no additional text):
{{
    "name": "Descriptive project name",
    "description": "Professional and detailed description based on ALL the conversation context",
    "experience_level": "Beginner|Intermediate|Advanced",
    "project_type": "Web|Mobile|Desktop|API|Data Science|DevOps|Other",
    "suggested_technologies": ["name1", "name2"],
    "reasoning": "Brief explanation of why these technologies and experience level are recommended, considering all the information provided",
    "recommendations": "COMPREHENSIVE and DETAILED recommendations for the project development. Include: architecture suggestions, technology stack rationale, best practices, security considerations, scalability advice, and development workflow recommendations. Minimum 5-6 sentences with specific, actionable advice.",
    "follow_up_questions": ["Question 1", "Question 2"] or [],
    "needs_more_info": true or false
}}

RULES:
- Use ALL the conversation history to build a complete understanding
- Only use technologies from the provided list
- Provide VERY DETAILED recommendations (this is important - be specific and actionable)
- If you have enough information to create a complete project specification, set needs_more_info to false
- If more details are needed, ask targeted follow-up questions
- Respond ONLY with the JSON, without additional text"""
    
    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-r1:1.5b"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode("utf-8").strip()
        
        # Limpiar el output: remover "Thinking..." y texto antes del JSON
        output_lower = output.lower()
        # Buscar el inicio del JSON
        json_start = output.find("{")
        
        # Si hay texto antes del JSON, intentar extraerlo
        if json_start > 0:
            # Buscar patrones comunes de "Thinking..." o texto introductorio
            if "thinking" in output_lower[:json_start] or "okay" in output_lower[:json_start]:
                # Intentar encontrar el JSON real más adelante
                for i in range(json_start, len(output)):
                    if output[i] == '{':
                        json_start = i
                        break
        
        # Intentar extraer JSON de la respuesta
        parsed = None
        json_text = None
        
        # Método 1: Buscar JSON completo
        json_end = output.rfind("}")
        if json_start >= 0 and json_end > json_start:
            json_text = output[json_start:json_end + 1]
            try:
                parsed = json.loads(json_text)
            except json.JSONDecodeError:
                pass
        
        # Método 2: Si falló, buscar cualquier bloque JSON en el texto
        if not parsed:
            import re
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.finditer(json_pattern, output, re.DOTALL)
            for match in matches:
                try:
                    parsed = json.loads(match.group())
                    json_text = match.group()
                    break
                except json.JSONDecodeError:
                    continue
        
        # Método 3: Extraer información del texto aunque no sea JSON perfecto
        if not parsed:
            # Intentar extraer información útil del texto
            parsed = extract_info_from_text(output, project_description, tech_names)
        
        # Validar y limpiar el resultado
        if parsed:
            # Validar que las tecnologías sugeridas existan en la base de datos
            valid_techs = []
            suggested = parsed.get("suggested_technologies", [])
            
            # Si no hay tecnologías sugeridas o son muy pocas, buscar en el texto
            if not suggested or len(suggested) < 2:
                # Buscar en el output de la IA y también en la descripción original
                suggested_output = find_technologies_in_text(output, tech_names)
                suggested_desc = find_technologies_in_text(project_description, tech_names)
                # Combinar y eliminar duplicados
                all_suggested = suggested_output + suggested_desc
                seen_ids = set()
                for tech in all_suggested:
                    if isinstance(tech, dict) and tech.get('id') not in seen_ids:
                        valid_techs.append(tech)
                        seen_ids.add(tech.get('id'))
            
            # Procesar tecnologías sugeridas por la IA (pueden ser strings o dicts)
            seen_ids = {tech.get('id') for tech in valid_techs if isinstance(tech, dict)}
            
            for tech_item in suggested:
                # Si ya es un diccionario válido, usarlo directamente
                if isinstance(tech_item, dict) and tech_item.get('id'):
                    if tech_item.get('id') not in seen_ids:
                        valid_techs.append(tech_item)
                        seen_ids.add(tech_item.get('id'))
                    continue
                
                # Si es un string, buscar la tecnología
                tech_name = tech_item if isinstance(tech_item, str) else str(tech_item)
                
                # Buscar tecnología exacta o similar
                tech = None
                # Primero búsqueda exacta (case insensitive)
                for t in technologies:
                    if t.name.lower() == tech_name.lower():
                        tech = t
                        break
                
                # Si no encuentra exacta, buscar parcial
                if not tech:
                    tech = Technology.query.filter(
                        Technology.name.ilike(f"%{tech_name}%")
                    ).first()
                
                if tech and tech.id not in seen_ids:
                    valid_techs.append(tech.to_dict())
                    seen_ids.add(tech.id)
            
            parsed["suggested_technologies"] = valid_techs
            
            # Ensure all required fields exist
            if not parsed.get("name"):
                parsed["name"] = extract_project_name(project_description)
            if not parsed.get("description"):
                parsed["description"] = project_description[:500] + "..." if len(project_description) > 500 else project_description
            if not parsed.get("experience_level") or parsed["experience_level"] not in ["Beginner", "Intermediate", "Advanced"]:
                parsed["experience_level"] = determine_experience_level(project_description)
            if not parsed.get("project_type") or parsed["project_type"] not in ["Web", "Mobile", "Desktop", "API", "Data Science", "DevOps", "Other"]:
                parsed["project_type"] = determine_project_type(project_description)
            
            # Ensure recommendations are present and detailed
            if not parsed.get("recommendations") or len(parsed.get("recommendations", "")) < 50:
                parsed["recommendations"] = generate_default_recommendations(parsed, project_description)
            
            # Ensure follow_up_questions exists
            if "follow_up_questions" not in parsed:
                parsed["follow_up_questions"] = []
            
            # Ensure needs_more_info exists
            if "needs_more_info" not in parsed:
                parsed["needs_more_info"] = len(parsed.get("follow_up_questions", [])) > 0
            
            return parsed
        else:
            # Fallback: crear respuesta básica con análisis simple
            return create_fallback_response(project_description, tech_names)
            
    except subprocess.TimeoutExpired:
        return {
            "error": "The AI query took too long. Please try again.",
            "name": extract_project_name(project_description),
            "description": project_description[:500] + "..." if len(project_description) > 500 else project_description,
            "experience_level": determine_experience_level(project_description),
            "project_type": determine_project_type(project_description),
            "suggested_technologies": find_technologies_in_text(project_description, tech_names),
            "reasoning": "Timeout in the AI query. A basic response was generated based on text analysis.",
            "recommendations": "Try to be more specific or divide your description into smaller parts."
        }
    except Exception as e:
        return {
            "error": f"Error querying the AI: {str(e)}",
            "name": extract_project_name(project_description),
            "description": project_description[:500] + "..." if len(project_description) > 500 else project_description,
            "experience_level": determine_experience_level(project_description),
            "project_type": determine_project_type(project_description),
            "suggested_technologies": find_technologies_in_text(project_description, tech_names),
            "reasoning": f"Error processing: {str(e)}",
            "recommendations": "Please review and manually adjust the fields."
        }

def extract_info_from_text(text, project_description, tech_names):
    """Extracts useful information from text even if it's not valid JSON"""
    result = {
        "name": extract_project_name(project_description),
        "description": project_description[:500] + "..." if len(project_description) > 500 else project_description,
        "experience_level": determine_experience_level(text + " " + project_description),
        "project_type": determine_project_type(text + " " + project_description),
        "suggested_technologies": find_technologies_in_text(text + " " + project_description, tech_names),
        "reasoning": "Information extracted from text analysis.",
        "recommendations": "Please review and adjust the suggestions according to your specific needs."
    }
    return result

def extract_project_name(description):
    """Extrae un nombre sugerido del proyecto desde la descripción"""
    import re
    # Buscar patrones como "Proyecto:", "Plataforma:", "## 🏠 Proyecto:", etc.
    patterns = [
        r'(?:##\s*)?(?:🏠|📱|💻)?\s*(?:Proyecto|Plataforma|Sistema|Aplicación)[:\s]+([^\n\.]+)',
        r'(?:##\s*)?([^\n\.]{3,60})\s*(?:-|:|\n)',
        r'^([A-ZÁÉÍÓÚÑ][^\n\.]{2,50})',
    ]
    for pattern in patterns:
        matches = re.finditer(pattern, description, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            name = match.group(1).strip()
            # Limpiar emojis y caracteres especiales al inicio
            name = re.sub(r'^[🏠📱💻⚙️💰🧱🎯\s]+', '', name)
            name = name.strip()
            if len(name) > 3 and len(name) < 100 and not name.startswith('#'):
                return name
    # Si no encuentra, usar primeras palabras relevantes
    lines = description.split('\n')
    for line in lines[:10]:  # Revisar primeras 10 líneas
        line = line.strip()
        if line and len(line) > 5 and len(line) < 100:
            # Si la línea parece un título
            if not line.startswith('#') and not line.startswith('-') and ':' not in line[:20]:
                words = line.split()[:8]
                if len(words) >= 2:
                    return " ".join(words)
    # Último recurso: primeras palabras
    words = description.split()[:5]
    return " ".join(words) if words else "Proyecto Nuevo"

def determine_experience_level(text):
    """Determina el nivel de experiencia basado en palabras clave"""
    text_lower = text.lower()
    advanced_keywords = ["avanzado", "complejo", "arquitectura", "microservicios", "scalable", "enterprise"]
    beginner_keywords = ["simple", "básico", "principiante", "fácil", "inicio"]
    
    if any(kw in text_lower for kw in advanced_keywords):
        return "Advanced"
    elif any(kw in text_lower for kw in beginner_keywords):
        return "Beginner"
    else:
        return "Intermediate"

def determine_project_type(text):
    """Determina el tipo de proyecto basado en palabras clave"""
    text_lower = text.lower()
    if any(kw in text_lower for kw in ["móvil", "mobile", "app movil", "android", "ios"]):
        return "Mobile"
    elif any(kw in text_lower for kw in ["api", "rest", "service", "backend"]):
        return "API"
    elif any(kw in text_lower for kw in ["data", "análisis", "machine learning", "ai"]):
        return "Data Science"
    elif any(kw in text_lower for kw in ["devops", "deploy", "infraestructura", "ci/cd"]):
        return "DevOps"
    elif any(kw in text_lower for kw in ["desktop", "escritorio", "aplicación de escritorio"]):
        return "Desktop"
    else:
        return "Web"

def find_technologies_in_text(text, available_techs):
    """Busca tecnologías mencionadas en el texto"""
    found_techs = []
    text_lower = text.lower()
    
    # Obtener todas las tecnologías de la base de datos
    technologies = Technology.query.order_by(Technology.name).all()
    tech_dict = {tech.name.lower(): tech for tech in technologies}
    
    # Buscar cada tecnología disponible en el texto
    for tech_name in available_techs:
        tech_lower = str(tech_name).lower()
        # Buscar la tecnología exacta o como palabra completa
        import re
        pattern = r'\b' + re.escape(tech_lower) + r'\b'
        if re.search(pattern, text_lower):
            # Buscar el objeto Technology completo
            if tech_lower in tech_dict:
                found_techs.append(tech_dict[tech_lower].to_dict())
            else:
                # Buscar parcialmente
                for tech_obj in technologies:
                    if tech_lower in tech_obj.name.lower() or tech_obj.name.lower() in tech_lower:
                        found_techs.append(tech_obj.to_dict())
                        break
    
    return found_techs

def create_fallback_response(project_description, tech_names):
    """Creates a fallback response when the AI doesn't respond correctly"""
    response = {
        "name": extract_project_name(project_description),
        "description": project_description[:500] + "..." if len(project_description) > 500 else project_description,
        "experience_level": determine_experience_level(project_description),
        "project_type": determine_project_type(project_description),
        "suggested_technologies": find_technologies_in_text(project_description, tech_names),
        "reasoning": "An automatic response was generated based on the analysis of the provided text.",
        "recommendations": generate_default_recommendations({
            "project_type": determine_project_type(project_description),
            "experience_level": determine_experience_level(project_description)
        }, project_description),
        "follow_up_questions": [
            "What specific features or functionalities are most important for your project?",
            "Do you have any technical constraints or preferences?",
            "What is your target audience or user base?"
        ],
        "needs_more_info": True
    }
    return response

def generate_default_recommendations(parsed, project_description):
    """Generates default recommendations when AI doesn't provide them"""
    project_type = parsed.get("project_type", "Web")
    experience_level = parsed.get("experience_level", "Intermediate")
    
    recommendations = f"For a {project_type} project at {experience_level} level, here are some recommendations:\n\n"
    
    if project_type == "Web":
        recommendations += "1. Consider using a modern frontend framework for better user experience and maintainability.\n"
        recommendations += "2. Implement responsive design to ensure your application works well on all devices.\n"
        recommendations += "3. Set up proper authentication and authorization mechanisms for user security.\n"
        recommendations += "4. Use a RESTful API architecture for better scalability and separation of concerns.\n"
        recommendations += "5. Implement proper error handling and logging for easier debugging and monitoring.\n"
    elif project_type == "Mobile":
        recommendations += "1. Choose between native, hybrid, or cross-platform development based on your needs.\n"
        recommendations += "2. Implement offline functionality for better user experience.\n"
        recommendations += "3. Consider push notifications for user engagement.\n"
        recommendations += "4. Optimize for different screen sizes and device capabilities.\n"
    else:
        recommendations += "1. Plan your architecture carefully to ensure scalability.\n"
        recommendations += "2. Implement proper error handling and logging.\n"
        recommendations += "3. Consider security best practices from the start.\n"
        recommendations += "4. Set up a proper development workflow with version control and testing.\n"
    
    recommendations += "\nIt's recommended to start with a minimum viable product (MVP) and iterate based on user feedback."
    
    return recommendations

@app.route('/ai-assistant', methods=['GET', 'POST'])
def ai_assistant():
    """AI Assistant page for creating projects"""
    technologies = Technology.query.order_by(Technology.name).all()
    return render_template('ai_assistant.html', technologies=technologies)

@app.route('/api/ai/analyze-project', methods=['POST'])
def api_analyze_project():
    """API endpoint para analizar proyecto con IA"""
    try:
        data = request.get_json()
        project_description = data.get('description', '').strip()
        project_goals = data.get('goals', '').strip()
        conversation_history = data.get('conversation_history', [])  # Historial de conversación
        
        if not project_description:
            return jsonify({
                'success': False,
                'error': 'La descripción del proyecto es requerida'
            }), 400
        
        # Analizar con IA (con historial de conversación)
        analysis = analyze_project_with_ai(project_description, project_goals, conversation_history)
        
        return jsonify({
            'success': True,
            'data': analysis
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al analizar proyecto: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting DevMatch AI Flask Server...")
    print("📱 Access the web interface at: http://localhost:3000")
    print("📊 Available pages:")
    print("   🏠 Homepage: http://localhost:3000")
    print("   🗂️  Projects: http://localhost:3000/projects")
    print("   👥 Developers: http://localhost:3000/developers")
    print("   🔍 Find Match: http://localhost:3000/matching")
    print("   🤖 AI Assistant: http://localhost:3000/ai-assistant")
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