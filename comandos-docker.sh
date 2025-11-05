#!/bin/bash

# Script de ayuda para Docker - DevMatch AI
# Uso: ./comandos-docker.sh [comando]

echo "🐳 DevMatch AI - Docker Helper Script"
echo "======================================"
echo ""

case "$1" in
    "start")
        echo "🚀 Starting all services..."
        docker-compose up -d
        echo ""
        echo "⏳ Waiting for services to be ready..."
        sleep 10
        echo ""
        echo "📊 Service status:"
        docker-compose ps
        echo ""
        echo "✅ Services started! Check logs with: ./comandos-docker.sh logs"
        ;;
    
    "stop")
        echo "🛑 Stopping all services..."
        docker-compose down
        echo "✅ Services stopped"
        ;;
    
    "restart")
        echo "🔄 Restarting all services..."
        docker-compose restart
        echo "✅ Services restarted"
        ;;
    
    "logs")
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    
    "logs-web")
        echo "📋 Web service logs:"
        docker-compose logs -f web
        ;;
    
    "logs-ollama")
        echo "📋 Ollama service logs:"
        docker-compose logs -f ollama
        ;;
    
    "logs-db")
        echo "📋 Database service logs:"
        docker-compose logs -f db
        ;;
    
    "status")
        echo "📊 Service status:"
        docker-compose ps
        echo ""
        echo "💾 Images:"
        docker images | grep -E "taller|python|postgres|ollama|adminer" || docker images
        echo ""
        echo "📦 Containers:"
        docker ps -a | grep taller || docker ps -a
        ;;
    
    "images")
        echo "🖼️  Docker images:"
        docker images
        ;;
    
    "containers")
        echo "📦 Docker containers:"
        docker ps -a
        ;;
    
    "pull-model")
        echo "📥 Pulling DeepSeek AI model..."
        docker-compose exec ollama ollama pull deepseek-r1:1.5b
        echo "✅ Model downloaded!"
        ;;
    
    "check-model")
        echo "🔍 Checking available AI models:"
        docker-compose exec ollama ollama list
        ;;
    
    "shell-web")
        echo "🐚 Opening shell in web container..."
        docker-compose exec web bash
        ;;
    
    "shell-db")
        echo "🐚 Opening shell in database container..."
        docker-compose exec db bash
        ;;
    
    "shell-ollama")
        echo "🐚 Opening shell in Ollama container..."
        docker-compose exec ollama sh
        ;;
    
    "clean")
        echo "🧹 Cleaning up..."
        docker system prune -f
        echo "✅ Cleanup complete"
        ;;
    
    "rebuild")
        echo "🔨 Rebuilding containers..."
        docker-compose build --no-cache
        echo "✅ Rebuild complete"
        ;;
    
    "stats")
        echo "📊 Container resource usage:"
        docker stats --no-stream
        ;;
    
    "help"|*)
        echo "Available commands:"
        echo ""
        echo "  start         - Start all services"
        echo "  stop          - Stop all services"
        echo "  restart       - Restart all services"
        echo "  logs          - Show all logs (follow mode)"
        echo "  logs-web      - Show web service logs"
        echo "  logs-ollama   - Show Ollama service logs"
        echo "  logs-db       - Show database service logs"
        echo "  status        - Show service status and info"
        echo "  images        - List all Docker images"
        echo "  containers    - List all containers"
        echo "  pull-model    - Download DeepSeek AI model"
        echo "  check-model   - Check available AI models"
        echo "  shell-web     - Open shell in web container"
        echo "  shell-db      - Open shell in database container"
        echo "  shell-ollama  - Open shell in Ollama container"
        echo "  clean         - Clean unused Docker resources"
        echo "  rebuild       - Rebuild all containers"
        echo "  stats         - Show container resource usage"
        echo "  help          - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./comandos-docker.sh start"
        echo "  ./comandos-docker.sh logs"
        echo "  ./comandos-docker.sh status"
        ;;
esac


