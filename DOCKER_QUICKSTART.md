# 🚀 Primeros Pasos con Docker - DevMatch AI

## ¡Empezemos! 

### 1. Verificar que Docker esté instalado
```bash
docker --version
docker-compose --version
```
Si no tienes Docker instalado, ve a https://www.docker.com/products/docker-desktop/

### 2. Construir y ejecutar el proyecto por primera vez

```bash
# Ir al directorio del proyecto
cd /Users/calebnehemias/taller

# Construir las imágenes Docker
docker-compose build

# Iniciar todos los servicios
docker-compose up
```

### 3. Acceder a tu aplicación

Una vez que veas el mensaje "Running on all addresses", abre tu navegador y ve a:

- **🌐 Aplicación principal**: http://localhost:5000
- **🗄️ Adminer (Base de datos)**: http://localhost:8080
  - Sistema: PostgreSQL
  - Servidor: db
  - Usuario: calebnehemias
  - Contraseña: password123
  - Base de datos: devmatch_ai

### 4. Usar el script de ayuda (más fácil)

```bash
# Hacer ejecutable (solo la primera vez)
chmod +x docker-helper.sh

# Usar comandos simples
./docker-helper.sh start    # Iniciar todo
./docker-helper.sh stop     # Parar todo
./docker-helper.sh logs     # Ver logs
./docker-helper.sh status   # Ver estado
./docker-helper.sh help     # Ver todos los comandos
```

### 5. Desarrollo diario

```bash
# Iniciar en segundo plano
./docker-helper.sh start

# Ver logs mientras desarrollas
./docker-helper.sh logs-web

# Parar cuando termines
./docker-helper.sh stop
```

### 6. Si algo sale mal

```bash
# Parar todo
docker-compose down

# Limpiar y empezar de nuevo
./docker-helper.sh clean
docker-compose build
docker-compose up
```

### 7. Comandos útiles

```bash
# Ver contenedores activos
docker ps

# Entrar al contenedor de la aplicación
docker-compose exec web bash

# Ver logs de un servicio específico
docker-compose logs web
docker-compose logs db

# Reiniciar solo un servicio
docker-compose restart web
```

## ¡Listo! 🎉

Tu aplicación DevMatch AI ahora está corriendo en Docker. Los cambios que hagas en tu código se reflejarán automáticamente sin necesidad de reiniciar (gracias a los volúmenes montados).

### Próximos pasos:
1. Ejecuta las migraciones de base de datos si es necesario
2. Carga datos de prueba
3. ¡Desarrolla tu aplicación!

### ¿Necesitas ayuda?
- Revisa el archivo `DOCKER_GUIDE.md` para más detalles
- Usa `./docker-helper.sh help` para ver todos los comandos disponibles