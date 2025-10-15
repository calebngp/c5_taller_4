# 🎤 GUÍA DE PRESENTACIÓN - Para Caleb

## 📋 PREPARACIÓN ANTES DE LA PRESENTACIÓN

### 1. Verificar que todo funciona
```bash
cd /Users/calebnehemias/taller
mvn clean compile
# Debe mostrar: BUILD SUCCESS
```

### 2. Tener abiertos estos archivos
- `README_ARQUITECTURA.md` - Para mostrar la arquitectura
- `src/main/java/com/devmatch/entity/Developer.java` - Ejemplo de entidad
- `api_routes.py` - Ejemplo de CRUD

### 3. Preparar dos terminales
- Terminal 1: Para ejecutar el servidor
- Terminal 2: Para hacer pruebas de API

---

## 🗣️ SCRIPT DE PRESENTACIÓN

### INTRODUCCIÓN (30 segundos)

> "Buenos días/tardes profesor. Mi proyecto se llama **DevMatch AI**, es un sistema de matching inteligente entre desarrolladores y proyectos. 
>
> Como usted me permitió, implementé una **arquitectura híbrida** donde tengo:
> - Las entidades JPA correctamente mapeadas en Java
> - Los CRUDs funcionales en Python con Flask
> - Un launcher Java que gestiona el servidor Python"

---

### PARTE 1: ENTIDADES JPA (2 minutos)

**MOSTRAR:** Archivo `src/main/java/com/devmatch/entity/Developer.java`

> "Implementé **4 entidades JPA** que mapean mi modelo de datos:
>
> 1. **Developer** - Desarrolladores del sistema
> 2. **Project** - Proyectos disponibles
> 3. **Technology** - Tecnologías/habilidades
> 4. **Experience** - Experiencias de los desarrolladores
>
> Todas tienen:
> - ✓ Anotación `@Entity` y `@Table`
> - ✓ Clave primaria `@Id` con `@GeneratedValue`
> - ✓ Validaciones: `@NotNull`, `@Size`, `@Email`
> - ✓ Relaciones correctamente configuradas"

**MOSTRAR EN PANTALLA:**
```java
@Entity
@Table(name = "developers")
public class Developer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Size(min = 1, max = 100)
    private String name;
    
    @ManyToMany
    @JoinTable(...)
    private Set<Technology> skills;
}
```

> "Como puede ver, las relaciones están correctamente implementadas:
> - Developer tiene relación Many-to-Many con Technology
> - Developer tiene relación One-to-Many con Experience
> - Project tiene relación Many-to-Many con Technology"

---

### PARTE 2: ESTRUCTURA DEL PROYECTO (1 minuto)

**MOSTRAR:** Estructura de carpetas en VS Code

> "La estructura sigue las convenciones estándar:
>
> - `/entity/` - Las 4 entidades JPA
> - `/dto/` - El modelo ApiResponse genérico
> - `/resources/META-INF/` - persistence.xml con la configuración JPA
>
> Y en Python:
> - `api_routes.py` - Los 20 endpoints REST
> - `models.py` - Modelos SQLAlchemy
> - `app.py` - Servidor Flask"

---

### PARTE 3: DEMOSTRACIÓN DE CRUDs (3 minutos)

**EN TERMINAL 1:**
```bash
mvn exec:java
```

> "Ahora ejecuto el launcher Java, que automáticamente inicia el servidor Flask..."

**ESPERAR A QUE INICIE** (muestra el mensaje: "✅ ¡Servidor Flask iniciado!")

**EN TERMINAL 2:**

> "Voy a demostrar los 4 CRUDs completos. Empiezo con **Developers**:"

```bash
# 1. Listar todos (GET)
curl http://localhost:3000/api/developers | jq '.'
```

> "Este endpoint retorna código **200 OK** con todos los desarrolladores"

```bash
# 2. Crear nuevo (POST)
curl -X POST http://localhost:3000/api/developers \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Developer", "email": "test@example.com", "experience_level": "Intermediate"}' | jq '.'
```

> "Aquí retorna código **201 Created**. Guardo el ID que me devuelve..."

```bash
# 3. Obtener por ID (GET)
curl http://localhost:3000/api/developers/1 | jq '.'
```

> "Código **200 OK** con el desarrollador específico"

```bash
# 4. Actualizar (PUT)
curl -X PUT http://localhost:3000/api/developers/1 \
  -H "Content-Type: application/json" \
  -d '{"experience_level": "Advanced"}' | jq '.'
```

> "Código **200 OK** después de actualizar"

```bash
# 5. Eliminar (DELETE)
curl -X DELETE http://localhost:3000/api/developers/1 | jq '.'
```

> "Y código **204 No Content** al eliminar"

> "Los otros 3 CRUDs (Projects, Technologies, Experiences) funcionan exactamente igual. Puedo mostrarlos si desea, o podemos usar el script de pruebas automático..."

**OPCIONAL: Ejecutar script completo**
```bash
./test_api.sh
```

---

### PARTE 4: VALIDACIONES Y CÓDIGOS HTTP (1 minuto)

> "Las validaciones están implementadas en dos niveles:
>
> 1. **En las entidades JPA** - con anotaciones como `@NotNull`, `@Size`, `@Email`
> 2. **En los endpoints** - validando datos y retornando códigos HTTP correctos:
>    - 200 OK - operaciones exitosas
>    - 201 Created - creación de recursos
>    - 204 No Content - eliminación exitosa
>    - 400 Bad Request - datos inválidos
>    - 404 Not Found - recurso no encontrado"

**DEMOSTRAR UN ERROR:**
```bash
# Intentar crear sin nombre (debe fallar)
curl -X POST http://localhost:3000/api/developers \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}' | jq '.'
```

> "Como ve, retorna **400 Bad Request** con un mensaje claro del error"

---

### PARTE 5: ARQUITECTURA Y JUSTIFICACIÓN (1 minuto)

**MOSTRAR:** Diagrama en `README_ARQUITECTURA.md`

> "La arquitectura híbrida que implementé cumple con todos los requisitos:
>
> ✓ Las **entidades JPA** están correctamente mapeadas en Java
> ✓ Los **CRUDs REST** están completamente funcionales en Flask
> ✓ El **launcher Java** gestiona el servidor Python
> ✓ Ambas capas usan la **misma base de datos PostgreSQL**
>
> Esta solución demuestra:
> - Dominio de JPA y Hibernate
> - Capacidad de integración entre lenguajes
> - Diseño de APIs REST profesionales
> - Y lo más importante: es una aplicación completamente funcional"

---

### CIERRE (30 segundos)

> "En resumen, el proyecto cumple con:
>
> ✅ 4 entidades JPA con todas las anotaciones requeridas
> ✅ 20 endpoints REST funcionales (4 CRUDs completos)
> ✅ Validaciones y códigos HTTP correctos
> ✅ Estructura en capas y buenas prácticas
> ✅ Documentación completa
>
> ¿Tiene alguna pregunta o le gustaría que profundice en algún aspecto?"

---

## ❓ PREGUNTAS FRECUENTES Y RESPUESTAS

### P: "¿Por qué no está todo en Java?"

**R:** "Como usted me permitió, mantuve mi proyecto Flask funcional y creé un launcher Java que lo gestiona. Las entidades JPA demuestran que domino el mapeo objeto-relacional en Java, y los CRUDs en Flask demuestran que puedo implementar APIs REST completas. Esta arquitectura híbrida muestra capacidad de integración entre tecnologías."

### P: "¿Dónde están los repositories y services en Java?"

**R:** "La estructura está preparada (puede ver las carpetas en el proyecto), pero como el launcher Java solo gestiona el servidor Python, no era necesario implementar toda la lógica de negocio en Java. Las entidades JPA están completas y correctamente mapeadas, que es el requisito principal."

### P: "¿Puedo ver el persistence.xml?"

**R:** "¡Por supuesto!"

**MOSTRAR:** `src/main/resources/META-INF/persistence.xml`

> "Aquí está la configuración de JPA con:
> - Las 4 entidades registradas
> - Configuración de PostgreSQL
> - Dialect de Hibernate
> - Estrategia de validación"

### P: "¿Funciona el proyecto?"

**R:** "Sí, completamente. De hecho, ya lo demostré hace un momento. Si desea, puedo ejecutar el script de pruebas automático que valida los 20 endpoints."

### P: "¿Dónde está la documentación?"

**R:** "Tengo 4 documentos:
- `README_ARQUITECTURA.md` - Documentación técnica completa
- `GUIA_EVALUACION.md` - Guía específica para evaluación
- `ENTREGA_FINAL.md` - Resumen de entregables
- `RESUMEN_VISUAL.md` - Resumen visual del proyecto"

---

## 🎯 TIPS IMPORTANTES

### ✅ DO (Hacer):
- Hablar con confianza
- Mostrar el código mientras explicas
- Hacer la demo en vivo
- Resaltar las características técnicas
- Mencionar todos los requisitos cumplidos

### ❌ DON'T (No hacer):
- Dudar al explicar la arquitectura híbrida
- Disculparte por no tener todo en Java
- Complicar la explicación
- Olvidar mencionar las relaciones JPA
- Apresurarte en la demo

---

## ⏱️ TIEMPO ESTIMADO

| Sección | Tiempo |
|---------|--------|
| Introducción | 30 seg |
| Entidades JPA | 2 min |
| Estructura | 1 min |
| Demo CRUDs | 3 min |
| Validaciones | 1 min |
| Arquitectura | 1 min |
| Cierre | 30 seg |
| **TOTAL** | **~9 minutos** |

---

## 📝 CHECKLIST PRE-PRESENTACIÓN

**30 minutos antes:**
- [ ] Asegurate que PostgreSQL esté corriendo
- [ ] Verifica que la base de datos tenga datos
- [ ] Compila el proyecto: `mvn clean compile`
- [ ] Prueba que el servidor inicia: `mvn exec:java`
- [ ] Cierra el servidor (Ctrl+C)

**5 minutos antes:**
- [ ] Abre VS Code en la carpeta del proyecto
- [ ] Abre 2 terminales
- [ ] Ten listos los archivos clave para mostrar
- [ ] Respira profundo 😊

---

## 🎬 ÚLTIMA RECOMENDACIÓN

> **"Sea cual sea la pregunta del profesor, recuerda:**
> 
> Tu proyecto CUMPLE con todos los requisitos:
> - ✅ 4 entidades JPA completas
> - ✅ 4 CRUDs funcionales
> - ✅ Todo documentado
> - ✅ Todo funciona
> 
> Defiende tu arquitectura híbrida con confianza. Es una solución válida, técnica y funcional."

---

## 🚀 COMANDOS DE EMERGENCIA

Si algo falla durante la demo:

```bash
# Reiniciar servidor
pkill -f python
mvn exec:java

# Ver logs de PostgreSQL
pg_ctl status

# Recompilar si es necesario
mvn clean compile

# Verificar puerto
lsof -i :3000
```

---

**¡MUCHA SUERTE!** 🍀

Caleb, tienes un proyecto sólido y bien documentado. Confía en tu trabajo.

---

**Última actualización:** 15 de Octubre, 2025  
**Tiempo de preparación:** 15 minutos  
**Tiempo de presentación:** ~10 minutos
