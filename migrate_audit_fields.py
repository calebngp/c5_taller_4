# ============================================================
# DevMatch AI - Migración de Campos de Auditoría
# Este script agrega los campos de auditoría a las tablas existentes
# ============================================================

import os
from flask import Flask
from models import db
from dotenv import load_dotenv
from sqlalchemy import text

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

def check_column_exists(connection, table_name, column_name):
    """Verifica si una columna existe en una tabla"""
    query = text("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = :table_name 
            AND column_name = :column_name
        )
    """)
    result = connection.execute(query, {"table_name": table_name, "column_name": column_name})
    return result.scalar()

def migrate_audit_fields():
    """Agrega los campos de auditoría a las tablas developers y projects"""
    app = create_app()
    
    with app.app_context():
        with db.engine.connect() as connection:
            print("🔍 Verificando estructura de la base de datos...")
            
            # Migrar tabla developers
            print("\n📊 Migrando tabla 'developers'...")
            columns_to_add = [
                ('usuario_creacion', 'VARCHAR(100)'),
                ('usuario_modificacion', 'VARCHAR(100)'),
                ('fecha_creacion', 'TIMESTAMP'),
                ('fecha_modificacion', 'TIMESTAMP')
            ]
            
            for column_name, column_type in columns_to_add:
                if not check_column_exists(connection, 'developers', column_name):
                    print(f"  ➕ Agregando columna 'developers.{column_name}'...")
                    alter_query = text(f"ALTER TABLE developers ADD COLUMN {column_name} {column_type}")
                    connection.execute(alter_query)
                    connection.commit()
                    print(f"  ✅ Columna 'developers.{column_name}' agregada exitosamente")
                else:
                    print(f"  ⏭️  Columna 'developers.{column_name}' ya existe, omitiendo...")
            
            # Migrar tabla projects
            print("\n📊 Migrando tabla 'projects'...")
            for column_name, column_type in columns_to_add:
                if not check_column_exists(connection, 'projects', column_name):
                    print(f"  ➕ Agregando columna 'projects.{column_name}'...")
                    alter_query = text(f"ALTER TABLE projects ADD COLUMN {column_name} {column_type}")
                    connection.execute(alter_query)
                    connection.commit()
                    print(f"  ✅ Columna 'projects.{column_name}' agregada exitosamente")
                else:
                    print(f"  ⏭️  Columna 'projects.{column_name}' ya existe, omitiendo...")
            
            print("\n✅ Migración de campos de auditoría completada exitosamente!")
            print("\n📋 Resumen:")
            print("   - Tabla 'developers': 4 columnas de auditoría verificadas/agregadas")
            print("   - Tabla 'projects': 4 columnas de auditoría verificadas/agregadas")
            print("\n💡 Los campos se actualizarán automáticamente en futuras operaciones CRUD")

if __name__ == '__main__':
    try:
        migrate_audit_fields()
    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
