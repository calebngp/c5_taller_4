# 🐳 Guía Completa de Docker - Desde Cero

Esta guía te enseñará todo lo que necesitas saber para usar Docker con tu proyecto DevMatch AI.

## 📚 Índice

1. [¿Qué es Docker?](#qué-es-docker)
2. [Instalación](#instalación)
3. [Conceptos Básicos](#conceptos-básicos)
4. [Comandos Esenciales](#comandos-esenciales)
5. [Ver Imágenes y Contenedores](#ver-imágenes-y-contenedores)
6. [Usar tu Proyecto](#usar-tu-proyecto)
7. [Solución de Problemas](#solución-de-problemas)

---

## ¿Qué es Docker?

Docker es una herramienta que permite empaquetar aplicaciones y todas sus dependencias en "contenedores". Es como una caja que contiene todo lo necesario para que tu aplicación funcione, sin importar dónde se ejecute.

### Analogía Simple:
- **Imagen**: Es como una plantilla o molde (ej: "plantilla de Python con Flask")
- **Contenedor**: Es una instancia ejecutándose de esa plantilla (ej: "mi aplicación corriendo")
- **Docker Compose**: Es como un director que coordina múltiples contenedores trabajando juntos

---

## Instalación

### En macOS:

1. **Descargar Docker Desktop:**
   - Ve a: https://www.docker.com/products/docker-desktop/
   - Descarga "Docker Desktop for Mac"
   - Instala la aplicación (arrastra a Applications)

2. **Abrir Docker Desktop:**
   - Busca "Docker" en Spotlight (Cmd + Espacio)
   - Abre Docker Desktop
   - Espera a que aparezca el ícono de ballena en la barra superior
   - ⚠️ Debe estar en verde (running) para funcionar

3. **Verificar instalación:**
   Abre Terminal y ejecuta:
   ```bash
   docker --version
   docker-compose --version
   ```
   
   Deberías ver algo como:
   ```
   Docker version 24.0.0
   docker-compose version 1.29.0
   ```

---

## Conceptos Básicos

### 1. **Imagen (Image)**
- Es un archivo de solo lectura que contiene todo lo necesario para ejecutar una aplicación
- Como una plantilla o receta
- Ejemplo: `python:3.11`, `postgres:15`, `ollama/ollama`

### 2. **Contenedor (Container)**
- Es una instancia ejecutándose de una imagen
- Es como una "caja" que corre tu aplicación
- Puedes tener múltiples contenedores de la misma imagen

### 3. **Volumen (Volume)**
- Es almacenamiento persistente
- Los datos en volúmenes NO se eliminan cuando borras contenedores
- Ejemplo: tu base de datos, modelos de IA

### 4. **Red (Network)**
- Permite que los contenedores se comuniquen entre sí
- Cada contenedor puede tener un "nombre" para comunicarse

---

## Comandos Esenciales

### Ver Información

#### Ver todas las imágenes:
```bash
docker images
```

**Salida típica:**
```
REPOSITORY          TAG       IMAGE ID       CREATED        SIZE
python              3.11      abc123def456   2 weeks ago    900MB
postgres            15        def456ghi789   1 week ago     380MB
ollama/ollama       latest    123abc456def   3 days ago     2.5GB
```

**Explicación:**
- **REPOSITORY**: Nombre de la imagen
- **TAG**: Versión (ej: "latest", "3.11")
- **IMAGE ID**: Identificador único
- **SIZE**: Tamaño en disco

#### Ver contenedores en ejecución:
```bash
docker ps
```

**Salida típica:**
```
CONTAINER ID   IMAGE              COMMAND                  STATUS         PORTS                    NAMES
a1b2c3d4e5f6   python:3.11       "python app.py"          Up 2 hours     0.0.0.0:3000->3000/tcp  taller_web_1
f6e5d4c3b2a1   postgres:15        "docker-entrypoint..."   Up 2 hours     0.0.0.0:5432->5432/tcp  taller_db_1
```

**Explicación:**
- **CONTAINER ID**: ID único del contenedor
- **IMAGE**: Imagen que usa
- **STATUS**: Estado (Up = corriendo, Exited = detenido)
- **PORTS**: Puertos mapeados (host:contenedor)
- **NAMES**: Nombre del contenedor

#### Ver TODOS los contenedores (incluyendo detenidos):
```bash
docker ps -a
```

#### Ver información detallada de una imagen:
```bash
docker image inspect python:3.11
```

#### Ver información de un contenedor:
```bash
docker inspect taller_web_1
```

#### Ver uso de recursos (CPU, memoria):
```bash
docker stats
```

**Salida:**
```
CONTAINER ID   NAME          CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
a1b2c3d4e5f6   taller_web_1  0.50%     150MiB / 4GiB         3.75%     1.2MB / 800KB
```

---

### Gestionar Contenedores

#### Iniciar un contenedor:
```bash
docker start nombre_contenedor
```

#### Detener un contenedor:
```bash
docker stop nombre_contenedor
```

#### Reiniciar un contenedor:
```bash
docker restart nombre_contenedor
```

#### Eliminar un contenedor:
```bash
docker rm nombre_contenedor
```

#### Eliminar un contenedor que está corriendo (forzado):
```bash
docker rm -f nombre_contenedor
```

---

### Gestionar Imágenes

#### Ver imágenes:
```bash
docker images
```

#### Eliminar una imagen:
```bash
docker rmi nombre_imagen
```

#### Eliminar imagen por ID:
```bash
docker rmi abc123def456
```

#### Eliminar imágenes no usadas:
```bash
docker image prune
```

#### Eliminar TODAS las imágenes no usadas:
```bash
docker image prune -a
```

---

### Ver Logs (Registros)

#### Ver logs de un contenedor:
```bash
docker logs nombre_contenedor
```

#### Ver logs en tiempo real (seguimiento):
```bash
docker logs -f nombre_contenedor
```

#### Ver últimas 50 líneas:
```bash
docker logs --tail 50 nombre_contenedor
```

---

### Ejecutar Comandos Dentro de Contenedores

#### Abrir terminal interactiva en un contenedor:
```bash
docker exec -it nombre_contenedor bash
```

#### Ejecutar un comando específico:
```bash
docker exec nombre_contenedor ls -la
```

#### Ejecutar Python en el contenedor:
```bash
docker exec -it taller_web_1 python
```

---

## Docker Compose (Múltiples Contenedores)

Docker Compose te permite gestionar múltiples contenedores a la vez.

### Comandos Principales

#### Iniciar todos los servicios:
```bash
docker-compose up
```

#### Iniciar en segundo plano (detached):
```bash
docker-compose up -d
```

#### Ver estado de servicios:
```bash
docker-compose ps
```

#### Ver logs de todos los servicios:
```bash
docker-compose logs
```

#### Ver logs de un servicio específico:
```bash
docker-compose logs web
docker-compose logs ollama
docker-compose logs db
```

#### Ver logs en tiempo real:
```bash
docker-compose logs -f
```

#### Detener todos los servicios:
```bash
docker-compose down
```

#### Detener y eliminar volúmenes (⚠️ borra datos):
```bash
docker-compose down -v
```

#### Reconstruir imágenes:
```bash
docker-compose build
```

#### Reconstruir y reiniciar:
```bash
docker-compose up --build
```

---

## Ver Imágenes y Contenedores

### Método 1: Terminal (Línea de Comandos)

#### Ver todas las imágenes:
```bash
docker images
```

#### Ver imágenes con filtro:
```bash
# Solo imágenes de Python
docker images python

# Solo imágenes de menos de 24 horas
docker images --filter "since=python:3.11"
```

#### Ver contenedores:
```bash
# Solo corriendo
docker ps

# Todos (incluyendo detenidos)
docker ps -a

# Formato compacto
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"
```

### Método 2: Docker Desktop (Interfaz Gráfica)

1. **Abrir Docker Desktop**
2. **Ver Imágenes:**
   - Click en "Images" en el menú lateral
   - Verás todas las imágenes descargadas
   - Puedes ver tamaño, cuándo se creó, etc.

3. **Ver Contenedores:**
   - Click en "Containers" en el menú lateral
   - Verás todos los contenedores
   - Puedes iniciar/detener desde aquí
   - Click en un contenedor para ver logs, estadísticas, etc.

4. **Ver Logs:**
   - Click en un contenedor
   - Pestaña "Logs" para ver los registros

5. **Ver Estadísticas:**
   - Click en un contenedor
   - Pestaña "Stats" para ver CPU, memoria, red

---

## Usar tu Proyecto DevMatch AI

### Paso 1: Verificar Docker

```bash
docker --version
docker-compose --version
```

### Paso 2: Navegar a tu proyecto

```bash
cd /Users/calebnehemias/taller
```

### Paso 3: Ver qué hay configurado

```bash
# Ver archivo de configuración
cat docker-compose.yml
```

### Paso 4: Iniciar el proyecto

```bash
# Primera vez (o si cambiaste dependencias)
docker-compose build

# Iniciar todos los servicios
docker-compose up -d
```

### Paso 5: Ver qué está corriendo

```bash
# Ver contenedores
docker-compose ps

# Ver logs
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs web
```

### Paso 6: Descargar el modelo de IA (solo primera vez)

```bash
# Esperar unos segundos para que Ollama esté listo
sleep 30

# Descargar el modelo
docker-compose exec ollama ollama pull deepseek-r1:1.5b
```

### Paso 7: Verificar que todo funciona

```bash
# Ver logs de la aplicación web
docker-compose logs -f web
```

Deberías ver algo como:
```
🚀 Starting DevMatch AI Flask Server...
📱 Access the web interface at: http://localhost:3000
```

### Paso 8: Acceder a la aplicación

- **Aplicación Web**: http://localhost:3000
- **Base de Datos (Adminer)**: http://localhost:8080
- **Ollama API**: http://localhost:11434

---

## Comandos Útiles para tu Proyecto

### Ver estado de todos los servicios:
```bash
docker-compose ps
```

### Ver logs en tiempo real:
```bash
docker-compose logs -f
```

### Ver logs solo de la aplicación web:
```bash
docker-compose logs -f web
```

### Reiniciar solo un servicio:
```bash
docker-compose restart web
docker-compose restart ollama
```

### Detener todo:
```bash
docker-compose down
```

### Ver qué imágenes se están usando:
```bash
docker images | grep -E "python|postgres|ollama|adminer"
```

### Ver qué contenedores están corriendo:
```bash
docker ps | grep taller
```

### Ejecutar un comando en el contenedor web:
```bash
# Abrir terminal en el contenedor
docker-compose exec web bash

# Ejecutar Python
docker-compose exec web python -c "print('Hello from Docker!')"

# Ver archivos
docker-compose exec web ls -la
```

### Verificar conexión a la base de datos:
```bash
docker-compose exec db psql -U calebnehemias -d devmatch_ai -c "SELECT version();"
```

### Verificar Ollama:
```bash
# Ver modelos disponibles
docker-compose exec ollama ollama list

# Probar Ollama
curl http://localhost:11434/api/tags
```

---

## Solución de Problemas

### Problema: "Cannot connect to Docker daemon"

**Solución:**
```bash
# Asegúrate de que Docker Desktop esté corriendo
# Busca el ícono de ballena en la barra superior
# Debe estar en verde
```

### Problema: "Port already in use"

**Solución:**
```bash
# Ver qué está usando el puerto 3000
lsof -i :3000

# O cambiar el puerto en docker-compose.yml
ports:
  - "3001:3000"  # Usa 3001 en lugar de 3000
```

### Problema: "No space left on device"

**Solución:**
```bash
# Limpiar imágenes no usadas
docker image prune

# Limpiar todo lo no usado
docker system prune

# Ver espacio usado
docker system df
```

### Problema: Contenedor no inicia

**Solución:**
```bash
# Ver logs del contenedor
docker-compose logs nombre_servicio

# Ver qué pasó
docker-compose ps -a

# Reconstruir
docker-compose build --no-cache
docker-compose up
```

### Problema: Ollama no responde

**Solución:**
```bash
# Verificar que Ollama está corriendo
docker-compose ps ollama

# Ver logs
docker-compose logs ollama

# Reiniciar Ollama
docker-compose restart ollama

# Verificar que el modelo está descargado
docker-compose exec ollama ollama list
```

### Problema: Base de datos no conecta

**Solución:**
```bash
# Verificar que la BD está corriendo
docker-compose ps db

# Ver logs
docker-compose logs db

# Verificar conexión
docker-compose exec db pg_isready -U calebnehemias
```

---

## Limpieza y Mantenimiento

### Limpiar contenedores detenidos:
```bash
docker container prune
```

### Limpiar imágenes no usadas:
```bash
docker image prune
```

### Limpiar TODO (⚠️ cuidado):
```bash
docker system prune -a
```

### Ver espacio usado:
```bash
docker system df
```

### Ver información detallada:
```bash
docker system info
```

---

## Tips y Mejores Prácticas

1. **Usa `docker-compose up -d`** para correr en segundo plano
2. **Revisa logs regularmente** con `docker-compose logs`
3. **No borres volúmenes** a menos que sepas lo que haces (`docker-compose down -v`)
4. **Limpia regularmente** imágenes no usadas para ahorrar espacio
5. **Usa Docker Desktop** para visualizar todo gráficamente
6. **Guarda tus datos** en volúmenes (no se pierden al borrar contenedores)

---

## Resumen de Comandos Más Usados

```bash
# Ver imágenes
docker images

# Ver contenedores
docker ps
docker ps -a

# Iniciar proyecto
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener proyecto
docker-compose down

# Reconstruir
docker-compose build
docker-compose up --build

# Limpiar
docker system prune
```

---

## Próximos Pasos

1. ✅ Instala Docker Desktop
2. ✅ Aprende los comandos básicos
3. ✅ Ejecuta tu proyecto: `docker-compose up -d`
4. ✅ Explora Docker Desktop para ver todo visualmente
5. ✅ Practica con los comandos

¡Ya estás listo para usar Docker! 🎉


