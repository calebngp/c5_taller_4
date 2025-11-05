# 🐳 Docker Setup Guide for DevMatch AI with Ollama

This guide explains how to run DevMatch AI with AI capabilities in Docker.

## 📋 Prerequisites

- Docker Desktop installed
- Docker Compose installed
- At least 8GB of RAM (recommended for Ollama)

## 🚀 Quick Start

### 1. Pull the DeepSeek model (first time only)

When you start the containers for the first time, you need to pull the AI model:

```bash
# Start all services
docker-compose up -d

# Wait for Ollama to be ready (about 30-60 seconds)

# Pull the DeepSeek model
docker-compose exec ollama ollama pull deepseek-r1:1.5b
```

### 2. Start all services

```bash
docker-compose up
```

Or in detached mode:

```bash
docker-compose up -d
```

### 3. Access the application

- **Web Application**: http://localhost:3000
- **Adminer (Database UI)**: http://localhost:8080
- **Ollama API**: http://localhost:11434

## 🏗️ Architecture

The Docker setup includes:

1. **PostgreSQL Database** (`db`)
   - Stores all application data
   - Persistent volume for data

2. **Ollama AI Service** (`ollama`)
   - Runs the DeepSeek AI model
   - Persistent volume for models
   - Accessible via API

3. **Flask Web Application** (`web`)
   - Main application
   - Connects to database and Ollama
   - Hot-reload enabled for development

4. **Adminer** (optional)
   - Web interface for database management

## 📦 Services

### PostgreSQL Database
- **Port**: 5432
- **Database**: devmatch_ai
- **User**: calebnehemias
- **Password**: password123

### Ollama AI Service
- **Port**: 11434
- **Model**: deepseek-r1:1.5b
- **Volume**: ollama_data (persists models)

### Flask Application
- **Port**: 3000
- **Environment**: Development (hot-reload enabled)
- **Dependencies**: Waits for database and Ollama to be ready

## 🔧 Configuration

### Environment Variables

You can customize the setup by creating a `.env` file:

```env
# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=devmatch_ai
DB_USER=calebnehemias
DB_PASSWORD=password123

# Ollama
OLLAMA_HOST=ollama
OLLAMA_PORT=11434

# Flask
FLASK_ENV=development
```

### Using Different AI Models

To use a different model:

1. Pull the model:
```bash
docker-compose exec ollama ollama pull <model-name>
```

2. Update `app.py` to use the new model name

## 🛠️ Common Commands

### Start services
```bash
docker-compose up
```

### Start in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs ollama
docker-compose logs db
```

### Rebuild containers
```bash
docker-compose build
docker-compose up
```

### Check Ollama models
```bash
docker-compose exec ollama ollama list
```

### Pull/update AI model
```bash
docker-compose exec ollama ollama pull deepseek-r1:1.5b
```

### Access database
```bash
docker-compose exec db psql -U calebnehemias -d devmatch_ai
```

### Run database migrations
```bash
docker-compose exec web python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 🔍 Troubleshooting

### Ollama not responding

1. Check if Ollama container is running:
```bash
docker-compose ps ollama
```

2. Check Ollama logs:
```bash
docker-compose logs ollama
```

3. Verify the model is pulled:
```bash
docker-compose exec ollama ollama list
```

4. If model is missing, pull it:
```bash
docker-compose exec ollama ollama pull deepseek-r1:1.5b
```

### Database connection errors

1. Check if database is ready:
```bash
docker-compose exec db pg_isready -U calebnehemias
```

2. Check database logs:
```bash
docker-compose logs db
```

3. Verify environment variables are correct

### Port conflicts

If ports are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "3001:3000"  # Change host port
```

### AI responses are slow

The first request may be slow as Ollama loads the model. Subsequent requests will be faster.

### Out of memory

Ollama requires significant RAM. If you encounter memory issues:

1. Reduce the model size (use a smaller model)
2. Increase Docker memory limit in Docker Desktop settings
3. Close other applications

## 📊 Monitoring

### Check service health
```bash
docker-compose ps
```

### View resource usage
```bash
docker stats
```

### Test Ollama API
```bash
curl http://localhost:11434/api/tags
```

## 🧹 Cleanup

### Remove all containers and volumes
```bash
docker-compose down -v
```

### Remove only containers (keep data)
```bash
docker-compose down
```

### Remove unused images
```bash
docker image prune
```

## 🔐 Security Notes

⚠️ **Important**: The default passwords are for development only. For production:

1. Change database passwords
2. Use Docker secrets or environment files
3. Don't expose Ollama port publicly
4. Use proper authentication

## 📝 Notes

- Models are stored in `ollama_data` volume and persist between restarts
- Database data is stored in `postgres_data` volume
- Code changes are reflected immediately (hot-reload enabled)
- First startup may take 1-2 minutes for all services to be ready


