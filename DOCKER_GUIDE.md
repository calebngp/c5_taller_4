# 🐳 Guía Completa de Docker para DevMatch AI

## 1. Instalación de Docker

### En macOS:
1. Ve a https://www.docker.com/products/docker-desktop/
2. Descarga Docker Desktop para Mac
3. Instala la aplicación
4. Abre Docker Desktop y espera a que inicie
5. Verifica la instalación:
   ```bash
   docker --version
   docker-compose --version
   ```

## 2. Conceptos Básicos

- **Imagen**: Un template de solo lectura para crear contenedores
- **Contenedor**: Una instancia ejecutable de una imagen
- **Dockerfile**: Archivo con instrucciones para crear una imagen
- **docker-compose**: Herramienta para manejar aplicaciones multi-contenedor

## 3. Estructura del Proyecto con Docker

Tu proyecto tendrá esta estructura:
```
taller/
├── Dockerfile              # Para la aplicación Python/Flask
├── docker-compose.yml      # Para orquestar todos los servicios
├── .dockerignore           # Archivos que Docker debe ignorar
├── app.py                  # Tu aplicación Flask
├── requirements.txt        # Dependencias Python
└── ... (resto de archivos)
```

## 4. Comandos Docker Básicos

### Imágenes:
```bash
# Ver imágenes descargadas
docker images

# Construir una imagen
docker build -t nombre-imagen .

# Eliminar una imagen
docker rmi nombre-imagen
```

### Contenedores:
```bash
# Ver contenedores activos
docker ps

# Ver todos los contenedores (activos e inactivos)
docker ps -a

# Ejecutar un contenedor
docker run nombre-imagen

# Parar un contenedor
docker stop id-contenedor

# Eliminar un contenedor
docker rm id-contenedor
```

### Docker Compose:
```bash
# Levantar todos los servicios
docker-compose up

# Levantar en segundo plano
docker-compose up -d

# Parar todos los servicios
docker-compose down

# Ver logs
docker-compose logs

# Reconstruir las imágenes
docker-compose build
```

## 5. Pasos para Dockerizar tu Proyecto

### Paso 1: Crear Dockerfile
### Paso 2: Crear docker-compose.yml
### Paso 3: Crear .dockerignore
### Paso 4: Variables de entorno
### Paso 5: Ejecutar el proyecto

## 6. Solución de Problemas Comunes

### Puerto ya en uso:
```bash
# Ver qué está usando el puerto 5000
sudo lsof -i :5000

# Matar proceso en puerto específico
kill -9 $(lsof -t -i:5000)
```

### Limpiar Docker:
```bash
# Eliminar contenedores parados
docker container prune

# Eliminar imágenes no utilizadas
docker image prune

# Limpiar todo (¡CUIDADO!)
docker system prune -a
```

### Ver logs de un contenedor específico:
```bash
docker-compose logs nombre-servicio
```

## 7. Tips Importantes

1. **Siempre usa .dockerignore** para evitar copiar archivos innecesarios
2. **Las variables de entorno** se manejan con archivos .env
3. **Los volúmenes** permiten persistir datos entre reinicios
4. **Los puertos** se mapean entre el contenedor y tu máquina
5. **Reconstruye** las imágenes cuando cambies dependencias

## 8. Flujo de Trabajo Diario

1. Hacer cambios en tu código
2. Si cambias requirements.txt: `docker-compose build`
3. Levantar servicios: `docker-compose up`
4. Desarrollar y probar
5. Parar servicios: `docker-compose down`