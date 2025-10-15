# ============================================================
# DevMatch AI - API REST Endpoints
# Este archivo contiene los endpoints API REST para los CRUDs
# ============================================================

from flask import Blueprint, jsonify, request
from models import db, Developer, Technology, Experience, Project

# Crear blueprint para la API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ============================================================
# CRUD: DEVELOPERS
# ============================================================

@api_bp.route('/developers', methods=['GET'])
def get_developers():
    """GET /api/developers - Listar todos los desarrolladores"""
    try:
        developers = Developer.query.all()
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Desarrolladores recuperados exitosamente',
            'data': [dev.to_dict() for dev in developers]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener desarrolladores: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/developers/<int:id>', methods=['GET'])
def get_developer(id):
    """GET /api/developers/<id> - Obtener un desarrollador por ID"""
    try:
        developer = Developer.query.get(id)
        if not developer:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Desarrollador con ID {id} no encontrado',
                'data': None
            }), 404
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Desarrollador encontrado',
            'data': developer.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener desarrollador: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/developers', methods=['POST'])
def create_developer():
    """POST /api/developers - Crear un nuevo desarrollador"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('name'):
            return jsonify({
                'success': False,
                'code': 400,
                'message': 'El nombre es requerido',
                'data': None
            }), 400
        
        # Crear desarrollador
        developer = Developer(
            name=data['name'],
            experience_level=data.get('experience_level', 'Beginner'),
            motivation=data.get('motivation', ''),
            email=data.get('email'),
            linkedin=data.get('linkedin'),
            github=data.get('github')
        )
        
        # Agregar habilidades si se proporcionaron
        if 'skills' in data:
            for tech_id in data['skills']:
                tech = Technology.query.get(tech_id)
                if tech:
                    developer.skills.append(tech)
        
        db.session.add(developer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 201,
            'message': 'Desarrollador creado exitosamente',
            'data': developer.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al crear desarrollador: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/developers/<int:id>', methods=['PUT'])
def update_developer(id):
    """PUT /api/developers/<id> - Actualizar un desarrollador"""
    try:
        developer = Developer.query.get(id)
        if not developer:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Desarrollador con ID {id} no encontrado',
                'data': None
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            developer.name = data['name']
        if 'experience_level' in data:
            developer.experience_level = data['experience_level']
        if 'motivation' in data:
            developer.motivation = data['motivation']
        if 'email' in data:
            developer.email = data['email']
        if 'linkedin' in data:
            developer.linkedin = data['linkedin']
        if 'github' in data:
            developer.github = data['github']
        
        # Actualizar habilidades si se proporcionaron
        if 'skills' in data:
            developer.skills.clear()
            for tech_id in data['skills']:
                tech = Technology.query.get(tech_id)
                if tech:
                    developer.skills.append(tech)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Desarrollador actualizado exitosamente',
            'data': developer.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al actualizar desarrollador: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/developers/<int:id>', methods=['DELETE'])
def delete_developer(id):
    """DELETE /api/developers/<id> - Eliminar un desarrollador"""
    try:
        developer = Developer.query.get(id)
        if not developer:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Desarrollador con ID {id} no encontrado',
                'data': None
            }), 404
        
        db.session.delete(developer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 204,
            'message': 'Desarrollador eliminado exitosamente',
            'data': None
        }), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al eliminar desarrollador: {str(e)}',
            'data': None
        }), 500

# ============================================================
# CRUD: PROJECTS
# ============================================================

@api_bp.route('/projects', methods=['GET'])
def get_projects():
    """GET /api/projects - Listar todos los proyectos"""
    try:
        projects = Project.query.all()
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Proyectos recuperados exitosamente',
            'data': [proj.to_dict() for proj in projects]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener proyectos: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    """GET /api/projects/<id> - Obtener un proyecto por ID"""
    try:
        project = Project.query.get(id)
        if not project:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Proyecto con ID {id} no encontrado',
                'data': None
            }), 404
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Proyecto encontrado',
            'data': project.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener proyecto: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/projects', methods=['POST'])
def create_project():
    """POST /api/projects - Crear un nuevo proyecto"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('name'):
            return jsonify({
                'success': False,
                'code': 400,
                'message': 'El nombre del proyecto es requerido',
                'data': None
            }), 400
        
        if not data.get('description'):
            return jsonify({
                'success': False,
                'code': 400,
                'message': 'La descripción es requerida',
                'data': None
            }), 400
        
        # Crear proyecto
        project = Project(
            name=data['name'],
            description=data['description'],
            experience_level=data.get('experience_level', 'Beginner'),
            project_type=data.get('project_type', 'Web'),
            status=data.get('status', 'Open')
        )
        
        # Agregar tecnologías si se proporcionaron
        if 'technologies' in data:
            for tech_id in data['technologies']:
                tech = Technology.query.get(tech_id)
                if tech:
                    project.required_technologies.append(tech)
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 201,
            'message': 'Proyecto creado exitosamente',
            'data': project.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al crear proyecto: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    """PUT /api/projects/<id> - Actualizar un proyecto"""
    try:
        project = Project.query.get(id)
        if not project:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Proyecto con ID {id} no encontrado',
                'data': None
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'experience_level' in data:
            project.experience_level = data['experience_level']
        if 'project_type' in data:
            project.project_type = data['project_type']
        if 'status' in data:
            project.status = data['status']
        
        # Actualizar tecnologías si se proporcionaron
        if 'technologies' in data:
            project.required_technologies.clear()
            for tech_id in data['technologies']:
                tech = Technology.query.get(tech_id)
                if tech:
                    project.required_technologies.append(tech)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Proyecto actualizado exitosamente',
            'data': project.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al actualizar proyecto: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    """DELETE /api/projects/<id> - Eliminar un proyecto"""
    try:
        project = Project.query.get(id)
        if not project:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Proyecto con ID {id} no encontrado',
                'data': None
            }), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 204,
            'message': 'Proyecto eliminado exitosamente',
            'data': None
        }), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al eliminar proyecto: {str(e)}',
            'data': None
        }), 500

# ============================================================
# CRUD: TECHNOLOGIES
# ============================================================

@api_bp.route('/technologies', methods=['GET'])
def get_technologies():
    """GET /api/technologies - Listar todas las tecnologías"""
    try:
        technologies = Technology.query.all()
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Tecnologías recuperadas exitosamente',
            'data': [tech.to_dict() for tech in technologies]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener tecnologías: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/technologies/<int:id>', methods=['GET'])
def get_technology(id):
    """GET /api/technologies/<id> - Obtener una tecnología por ID"""
    try:
        technology = Technology.query.get(id)
        if not technology:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Tecnología con ID {id} no encontrada',
                'data': None
            }), 404
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Tecnología encontrada',
            'data': technology.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener tecnología: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/technologies', methods=['POST'])
def create_technology():
    """POST /api/technologies - Crear una nueva tecnología"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('name'):
            return jsonify({
                'success': False,
                'code': 400,
                'message': 'El nombre de la tecnología es requerido',
                'data': None
            }), 400
        
        # Verificar si ya existe
        existing = Technology.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({
                'success': False,
                'code': 400,
                'message': f'La tecnología {data["name"]} ya existe',
                'data': None
            }), 400
        
        # Crear tecnología
        technology = Technology(
            name=data['name'],
            category=data.get('category', 'Other')
        )
        
        db.session.add(technology)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 201,
            'message': 'Tecnología creada exitosamente',
            'data': technology.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al crear tecnología: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/technologies/<int:id>', methods=['PUT'])
def update_technology(id):
    """PUT /api/technologies/<id> - Actualizar una tecnología"""
    try:
        technology = Technology.query.get(id)
        if not technology:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Tecnología con ID {id} no encontrada',
                'data': None
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            technology.name = data['name']
        if 'category' in data:
            technology.category = data['category']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Tecnología actualizada exitosamente',
            'data': technology.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al actualizar tecnología: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/technologies/<int:id>', methods=['DELETE'])
def delete_technology(id):
    """DELETE /api/technologies/<id> - Eliminar una tecnología"""
    try:
        technology = Technology.query.get(id)
        if not technology:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Tecnología con ID {id} no encontrada',
                'data': None
            }), 404
        
        db.session.delete(technology)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 204,
            'message': 'Tecnología eliminada exitosamente',
            'data': None
        }), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al eliminar tecnología: {str(e)}',
            'data': None
        }), 500

# ============================================================
# CRUD: EXPERIENCES
# ============================================================

@api_bp.route('/experiences', methods=['GET'])
def get_experiences():
    """GET /api/experiences - Listar todas las experiencias"""
    try:
        experiences = Experience.query.all()
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Experiencias recuperadas exitosamente',
            'data': [exp.to_dict() for exp in experiences]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener experiencias: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/experiences/<int:id>', methods=['GET'])
def get_experience(id):
    """GET /api/experiences/<id> - Obtener una experiencia por ID"""
    try:
        experience = Experience.query.get(id)
        if not experience:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Experiencia con ID {id} no encontrada',
                'data': None
            }), 404
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Experiencia encontrada',
            'data': experience.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al obtener experiencia: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/experiences', methods=['POST'])
def create_experience():
    """POST /api/experiences - Crear una nueva experiencia"""
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('description'):
            return jsonify({
                'success': False,
                'code': 400,
                'message': 'La descripción es requerida',
                'data': None
            }), 400
        
        if not data.get('developer_id'):
            return jsonify({
                'success': False,
                'code': 400,
                'message': 'El ID del desarrollador es requerido',
                'data': None
            }), 400
        
        # Verificar que el desarrollador existe
        developer = Developer.query.get(data['developer_id'])
        if not developer:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Desarrollador con ID {data["developer_id"]} no encontrado',
                'data': None
            }), 404
        
        # Crear experiencia
        experience = Experience(
            description=data['description'],
            category=data.get('category', 'project'),
            developer_id=data['developer_id']
        )
        
        db.session.add(experience)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 201,
            'message': 'Experiencia creada exitosamente',
            'data': experience.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al crear experiencia: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/experiences/<int:id>', methods=['PUT'])
def update_experience(id):
    """PUT /api/experiences/<int:id> - Actualizar una experiencia"""
    try:
        experience = Experience.query.get(id)
        if not experience:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Experiencia con ID {id} no encontrada',
                'data': None
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'description' in data:
            experience.description = data['description']
        if 'category' in data:
            experience.category = data['category']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 200,
            'message': 'Experiencia actualizada exitosamente',
            'data': experience.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al actualizar experiencia: {str(e)}',
            'data': None
        }), 500

@api_bp.route('/experiences/<int:id>', methods=['DELETE'])
def delete_experience(id):
    """DELETE /api/experiences/<id> - Eliminar una experiencia"""
    try:
        experience = Experience.query.get(id)
        if not experience:
            return jsonify({
                'success': False,
                'code': 404,
                'message': f'Experiencia con ID {id} no encontrada',
                'data': None
            }), 404
        
        db.session.delete(experience)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'code': 204,
            'message': 'Experiencia eliminada exitosamente',
            'data': None
        }), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'code': 500,
            'message': f'Error al eliminar experiencia: {str(e)}',
            'data': None
        }), 500
