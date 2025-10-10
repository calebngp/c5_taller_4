# ============================================================
# DevMatch AI - Flask Web Server
# ============================================================

from flask import Flask, render_template, request, jsonify, redirect, url_for
from modelai3 import projects as projects_data, developers as developers_data, calculate_match, analyze_with_deepseek

app = Flask(__name__)

@app.route('/')
def index():
    """Main route - Homepage with system overview"""
    return render_template('index.html', projects=projects_data, developers=developers_data)

@app.route('/projects')
def projects():
    """Projects listing page"""
    return render_template('projects.html', projects=projects_data)

@app.route('/developers')
def developers():
    """Developers listing page"""
    return render_template('developers.html', developers=developers_data)

@app.route('/matching')
def matching():
    """Matching page where users can select project and find candidates"""
    project_id = request.args.get('project_id', type=int)
    selected_project = None
    results = []
    
    if project_id:
        selected_project = next((p for p in projects_data if p["id"] == project_id), None)
        if selected_project:
            # Perform matching analysis
            for dev in developers_data:
                technical_match = calculate_match(selected_project, dev)
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
                         projects=projects_data, 
                         selected_project=selected_project, 
                         results=results)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    """Show detailed information for a specific project"""
    project = next((p for p in projects_data if p["id"] == project_id), None)
    if not project:
        return "Project not found", 404
    
    # Generate matches for this project
    matches = []
    for dev in developers_data:
        technical_match = calculate_match(project, dev)
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
    developer = next((d for d in developers_data if d["id"] == developer_id), None)
    if not developer:
        return "Developer not found", 404
    
    return render_template('developer_detail.html', 
                         developer=developer, 
                         projects=projects_data, 
                         calculate_match=calculate_match)

@app.route('/api/results')
def api_results():
    """API endpoint that returns JSON results"""
    results = []
    
    for project in projects_data:
        project_results = {
            "project": project,
            "matches": []
        }
        
        for dev in developers_data:
            score = calculate_match(project, dev)
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