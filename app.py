# ============================================================
# DevMatch AI - Flask Web Server
# ============================================================

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db
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

@app.route('/developers')
def developers():
    """Developers listing page"""
    developers_list = get_all_developers()
    return render_template('developers.html', developers=developers_list)

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
    print("📱 Access the web interface at: http://localhost:5001")
    print("📊 Available pages:")
    print("   🏠 Homepage: http://localhost:5001")
    print("   🗂️  Projects: http://localhost:5001/projects")
    print("   👥 Developers: http://localhost:5001/developers")
    print("   🔍 Find Match: http://localhost:5001/matching")
    print("   📊 API: http://localhost:5001/api/results")
    print("\n✨ Features:")
    print("   - AI-powered matching with DeepSeek")
    print("   - Interactive project-developer matching")
    print("   - Detailed profiles and compatibility analysis")
    print("   - Responsive web design")
    
    app.run(debug=True, host='0.0.0.0', port=5001)