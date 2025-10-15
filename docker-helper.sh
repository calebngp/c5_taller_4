#!/bin/bash

# Script para facilitar el uso de Docker en el proyecto DevMatch AI

echo "🐳 DevMatch AI - Docker Helper"
echo "=============================="

show_help() {
    echo "Uso: ./docker-helper.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start     - Iniciar todos los servicios"
    echo "  stop      - Parar todos los servicios"
    echo "  restart   - Reiniciar todos los servicios"
    echo "  build     - Construir las imágenes"
    echo "  logs      - Ver logs de todos los servicios"
    echo "  logs-web  - Ver logs solo de la aplicación web"
    echo "  logs-db   - Ver logs solo de la base de datos"
    echo "  clean     - Limpiar contenedores e imágenes no utilizadas"
    echo "  shell     - Abrir shell en el contenedor web"
    echo "  db-shell  - Abrir psql en la base de datos"
    echo "  status    - Ver estado de los contenedores"
    echo "  help      - Mostrar esta ayuda"
}

case $1 in
    "start")
        echo "🚀 Iniciando servicios..."
        docker-compose up -d
        echo "✅ Servicios iniciados!"
        echo "🌐 Aplicación web: http://localhost:3000"
        echo "🗄️  Adminer (DB): http://localhost:8080"
        ;;
    "stop")
        echo "🛑 Parando servicios..."
        docker-compose down
        echo "✅ Servicios parados!"
        ;;
    "restart")
        echo "🔄 Reiniciando servicios..."
        docker-compose down
        docker-compose up -d
        echo "✅ Servicios reiniciados!"
        ;;
    "build")
        echo "🏗️  Construyendo imágenes..."
        docker-compose build
        echo "✅ Imágenes construidas!"
        ;;
    "logs")
        docker-compose logs -f
        ;;
    "logs-web")
        docker-compose logs -f web
        ;;
    "logs-db")
        docker-compose logs -f db
        ;;
    "clean")
        echo "🧹 Limpiando Docker..."
        docker container prune -f
        docker image prune -f
        echo "✅ Limpieza completada!"
        ;;
    "shell")
        echo "🐚 Abriendo shell en contenedor web..."
        docker-compose exec web bash
        ;;
    "db-shell")
        echo "🗄️  Abriendo psql..."
        docker-compose exec db psql -U calebnehemias -d devmatch_ai
        ;;
    "status")
        echo "📊 Estado de los contenedores:"
        docker-compose ps
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo "❌ Comando desconocido: $1"
        echo ""
        show_help
        ;;
esac