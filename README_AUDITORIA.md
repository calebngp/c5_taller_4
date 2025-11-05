# 📋 Implementación de Campos de Auditoría - DevMatch AI

## 📌 Objetivos Cumplidos

Este documento explica la implementación de campos de auditoría en las entidades del proyecto DevMatch AI, cumpliendo con los requisitos académicos de:

- ✅ Comprender el concepto y propósito de la auditoría en bases de datos
- ✅ Aplicar buenas prácticas de persistencia en JPA y SQLAlchemy
- ✅ Implementar campos de trazabilidad para operaciones de creación y modificación
- ✅ Demostrar el uso de eventos automáticos para mantener valores actualizados

---

## 🏗️ Arquitectura Híbrida del Sistema

**DevMatch AI** es un sistema híbrido que utiliza:

- **Java JPA (Hibernate)**: Entidades para validación y documentación del esquema
- **Python SQLAlchemy (Flask)**: Modelos operativos que realizan las operaciones CRUD reales

La auditoría está implementada en **ambos sistemas** para garantizar coherencia:

1. **Entidades JPA Java** (`src/main/java/com/devmatch/entity/`)
   - Callbacks JPA: `@PrePersist` y `@PreUpdate`
   - Validación del esquema de base de datos

2. **Modelos SQLAlchemy Python** (`models.py`)
   - Eventos SQLAlchemy: `@event.listens_for` con `before_insert` y `before_update`
   - Operaciones CRUD reales desde Flask

---

## 🎯 Entidades Seleccionadas

Se implementaron campos de auditoría en las siguientes **dos entidades principales** del sistema:

1. **`Developer`** (Desarrollador)
   - **Java**: `src/main/java/com/devmatch/entity/Developer.java`
   - **Python**: `models.py` - clase `Developer`
   - Representa los desarrolladores registrados en el sistema
   - Entidad crítica para el sistema de matching

2. **`Project`** (Proyecto)
   - **Java**: `src/main/java/com/devmatch/entity/Project.java`
   - **Python**: `models.py` - clase `Project`
   - Representa los proyectos disponibles en el sistema
   - Entidad principal para el proceso de matching

---

## 🔧 Campos de Auditoría Implementados

Cada entidad ahora incluye los siguientes **4 campos de auditoría**, implementados tanto en Java JPA como en Python SQLAlchemy:

### En Java JPA

```java
@Column(name = "usuario_creacion", length = 100)
private String usuarioCreacion;

@Column(name = "usuario_modificacion", length = 100)
private String usuarioModificacion;

@Column(name = "fecha_creacion")
private LocalDateTime fechaCreacion;

@Column(name = "fecha_modificacion")
private LocalDateTime fechaModificacion;
```

### En Python SQLAlchemy

```python
usuario_creacion: Mapped[str] = mapped_column(String(100), nullable=True)
usuario_modificacion: Mapped[str] = mapped_column(String(100), nullable=True)
fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
fecha_modificacion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
```

### Tipos de Datos Utilizados

- **`usuarioCreacion` / `usuarioModificacion`**: 
  - Java: `String` (longitud máxima: 100 caracteres)
  - Python: `str` con `String(100)` (longitud máxima: 100 caracteres)

- **`fechaCreacion` / `fechaModificacion`**: 
  - Java: `LocalDateTime` (tipo estándar de Java 8+ para fechas y horas)
  - Python: `datetime` con `DateTime` (tipo de SQLAlchemy que mapea a TIMESTAMP en PostgreSQL)

> **Nota**: Se eligió `LocalDateTime`/`DateTime` porque son los tipos recomendados para JPA/Hibernate y SQLAlchemy respectivamente con PostgreSQL, y proporcionan mejor soporte de zona horaria que `Timestamp` o `Instant` para este caso de uso.

---

## ⚙️ Lógica Automática de Auditoría

### 1. Implementación en Java JPA (Callbacks JPA)

La actualización automática de los campos de auditoría se realiza mediante **callbacks del ciclo de vida de JPA**:

#### `@PrePersist` - Al Crear un Registro

```java
@PrePersist
protected void onCreate() {
    fechaCreacion = LocalDateTime.now();
    if (usuarioCreacion == null || usuarioCreacion.isEmpty()) {
        usuarioCreacion = System.getProperty("user.name", "system");
    }
}
```

**Comportamiento:**
- Se ejecuta **automáticamente** antes de insertar un nuevo registro en la base de datos
- Asigna `fechaCreacion` con la fecha y hora actual del sistema
- Asigna `usuarioCreacion` con el nombre del usuario del sistema (o "system" si no está disponible)
- Solo se ejecuta cuando se crea un **nuevo** registro (operación `persist()`)

#### `@PreUpdate` - Al Modificar un Registro

```java
@PreUpdate
protected void onUpdate() {
    fechaModificacion = LocalDateTime.now();
    usuarioModificacion = System.getProperty("user.name", "system");
}
```

**Comportamiento:**
- Se ejecuta **automáticamente** antes de actualizar un registro existente en la base de datos
- Actualiza `fechaModificacion` con la fecha y hora actual del sistema
- Actualiza `usuarioModificacion` con el nombre del usuario del sistema
- Solo se ejecuta cuando se **modifica** un registro existente (operación `merge()` o `update()`)

---

### 2. Implementación en Python SQLAlchemy (Eventos SQLAlchemy)

Como el sistema realiza las operaciones CRUD desde Python/Flask, también se implementó la auditoría usando **eventos de SQLAlchemy**:

#### `before_insert` - Al Crear un Registro

```python
@event.listens_for(Developer, 'before_insert')
def set_developer_audit_on_insert(mapper, connection, target):
    """Evento que se ejecuta antes de insertar un Developer"""
    target.fecha_creacion = datetime.now()
    if not target.usuario_creacion:
        target.usuario_creacion = get_current_user()
```

**Comportamiento:**
- Se ejecuta **automáticamente** antes de insertar un nuevo registro en la base de datos
- Asigna `fecha_creacion` con la fecha y hora actual del sistema
- Asigna `usuario_creacion` con el usuario del sistema (o "system" si no está disponible)
- Se ejecuta en todas las operaciones `db.session.add()` seguidas de `commit()`

#### `before_update` - Al Modificar un Registro

```python
@event.listens_for(Developer, 'before_update')
def set_developer_audit_on_update(mapper, connection, target):
    """Evento que se ejecuta antes de actualizar un Developer"""
    target.fecha_modificacion = datetime.now()
    target.usuario_modificacion = get_current_user()
```

**Comportamiento:**
- Se ejecuta **automáticamente** antes de actualizar un registro existente en la base de datos
- Actualiza `fecha_modificacion` con la fecha y hora actual del sistema
- Actualiza `usuario_modificacion` con el usuario del sistema
- Se ejecuta en todas las modificaciones seguidas de `db.session.commit()`

**Función auxiliar para obtener el usuario:**
```python
def get_current_user():
    """Obtiene el usuario actual del sistema o usa un valor por defecto"""
    return os.getenv('USER') or os.getenv('USERNAME') or 'system'
```

---

## 📊 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────┐
│                    OPERACIÓN CRUD                        │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   ¿Es una operación INSERT?    │
        └───────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
           SÍ                      NO
            │                       │
            ▼                       ▼
    ┌───────────────┐      ┌───────────────┐
    │ @PrePersist   │      │ @PreUpdate    │
    │ onCreate()    │      │ onUpdate()    │
    └───────────────┘      └───────────────┘
            │                       │
            │                       │
            ▼                       ▼
    ┌──────────────────┐   ┌──────────────────┐
    │ fechaCreacion    │   │ fechaModificacion│
    │ usuarioCreacion  │   │ usuarioModificacion│
    └──────────────────┘   └──────────────────┘
            │                       │
            └───────────┬───────────┘
                        ▼
            ┌───────────────────────┐
            │   GUARDAR EN BD       │
            └───────────────────────┘
```

---

## 💻 Ejemplo de Uso

### Desde Python/Flask (Operaciones Reales)

Como el sistema híbrido realiza las operaciones CRUD desde Python, aquí están los ejemplos prácticos:

#### Crear un Nuevo Developer

```python
from models import db, Developer

# Crear desarrollador
developer = Developer(
    name="Juan Pérez",
    email="juan@example.com",
    experience_level="Advanced"
)

# No es necesario asignar fecha_creacion ni usuario_creacion
# SQLAlchemy lo hará automáticamente mediante el evento before_insert

db.session.add(developer)
db.session.commit()

# Después del commit:
# - developer.fecha_creacion contiene la fecha/hora de creación
# - developer.usuario_creacion contiene el usuario del sistema
```

#### Modificar un Developer Existente

```python
developer = Developer.query.get(1)
developer.name = "Juan Carlos Pérez"  # Cambiar el nombre

# No es necesario actualizar fecha_modificacion ni usuario_modificacion
# SQLAlchemy lo hará automáticamente mediante el evento before_update

db.session.commit()

# Después del commit:
# - developer.fecha_modificacion contiene la fecha/hora de modificación
# - developer.usuario_modificacion contiene el usuario que modificó
```

#### Crear un Nuevo Project

```python
from models import db, Project

project = Project(
    name="Aplicación Web Moderna",
    description="Desarrollo de aplicación web con React y Node.js",
    experience_level="Intermediate",
    project_type="Web"
)

db.session.add(project)
db.session.commit()
# fecha_creacion y usuario_creacion se asignan automáticamente
```

#### Modificar un Project Existente

```python
project = Project.query.get(1)
project.status = "In Progress"

db.session.commit()
# fecha_modificacion y usuario_modificacion se actualizan automáticamente
```

### Desde Java JPA (Para Referencia)

Si se usara directamente desde Java (aunque no es el caso en este sistema):

```java
EntityManager em = // ... obtener EntityManager

Developer dev = new Developer();
dev.setName("Juan Pérez");
dev.setEmail("juan@example.com");
dev.setExperienceLevel("Advanced");

// No es necesario asignar fechaCreacion ni usuarioCreacion
// JPA lo hará automáticamente al hacer persist()

em.persist(dev);
em.getTransaction().commit();

// Después del commit:
// - dev.getFechaCreacion() contiene la fecha/hora de creación
// - dev.getUsuarioCreacion() contiene el usuario del sistema
```

---

## 🗄️ Estructura de la Base de Datos

### Tabla `developers`

```sql
CREATE TABLE developers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    -- ... otros campos ...
    
    -- Campos de auditoría
    usuario_creacion VARCHAR(100),
    usuario_modificacion VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_modificacion TIMESTAMP
);
```

### Tabla `projects`

```sql
CREATE TABLE projects (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    -- ... otros campos ...
    
    -- Campos de auditoría
    usuario_creacion VARCHAR(100),
    usuario_modificacion VARCHAR(100),
    fecha_creacion TIMESTAMP,
    fecha_modificacion TIMESTAMP
);
```

> **Nota**: Si la base de datos ya existe, será necesario ejecutar una migración para agregar estas columnas. Hibernate puede hacerlo automáticamente si se configura `hibernate.hbm2ddl.auto=update` (solo en desarrollo).

---

## 🔍 Beneficios de la Implementación

### 1. **Trazabilidad Completa**
- Registro de quién y cuándo se creó cada entidad
- Registro de quién y cuándo se modificó cada entidad
- Historial de cambios sin necesidad de tablas de auditoría separadas

### 2. **Automatización**
- No requiere intervención manual del desarrollador
- Los campos se actualizan automáticamente en cada operación
- Reduce errores humanos (olvidos de actualizar campos)

### 3. **Buenas Prácticas JPA**
- Uso de callbacks del ciclo de vida (`@PrePersist`, `@PreUpdate`)
- Separación de responsabilidades (la entidad maneja su propia auditoría)
- Compatible con cualquier proveedor JPA (Hibernate, EclipseLink, etc.)

### 4. **Cumplimiento de Requisitos Académicos**
- ✅ Demuestra comprensión de auditoría en bases de datos
- ✅ Aplica buenas prácticas de persistencia JPA
- ✅ Implementa lógica automática mediante eventos
- ✅ Mantiene valores actualizados sin intervención manual

---

## 📝 Consideraciones Técnicas

### Obtención del Usuario

Actualmente, la implementación obtiene el usuario mediante:
```java
System.getProperty("user.name", "system")
```

**En un entorno de producción**, se recomienda:
- Integrar con un sistema de autenticación (Spring Security, Java EE Security, etc.)
- Usar un contexto de seguridad para obtener el usuario autenticado
- O pasar el usuario como parámetro en los métodos de servicio

### Manejo de Zona Horaria

`LocalDateTime` no incluye información de zona horaria. Si es necesario:
- Usar `ZonedDateTime` para zonas horarias específicas
- O usar `Instant` para timestamps UTC

### Migraciones de Base de Datos

Para agregar estos campos a una base de datos existente, hay dos opciones:

#### Opción 1: Script de Migración Automático (Recomendado)

Se ha creado un script de migración Python que agrega las columnas de forma segura:

```bash
python migrate_audit_fields.py
```

Este script:
- ✅ Verifica si las columnas ya existen antes de agregarlas
- ✅ Es seguro ejecutarlo múltiples veces (idempotente)
- ✅ No afecta los datos existentes
- ✅ Muestra un resumen de las operaciones realizadas

#### Opción 2: Migración Manual con SQL

Si prefieres ejecutar la migración manualmente:

```sql
-- Tabla developers
ALTER TABLE developers 
ADD COLUMN IF NOT EXISTS usuario_creacion VARCHAR(100),
ADD COLUMN IF NOT EXISTS usuario_modificacion VARCHAR(100),
ADD COLUMN IF NOT EXISTS fecha_creacion TIMESTAMP,
ADD COLUMN IF NOT EXISTS fecha_modificacion TIMESTAMP;

-- Tabla projects
ALTER TABLE projects 
ADD COLUMN IF NOT EXISTS usuario_creacion VARCHAR(100),
ADD COLUMN IF NOT EXISTS usuario_modificacion VARCHAR(100),
ADD COLUMN IF NOT EXISTS fecha_creacion TIMESTAMP,
ADD COLUMN IF NOT EXISTS fecha_modificacion TIMESTAMP;
```

> **Nota**: El uso de `IF NOT EXISTS` en PostgreSQL previene errores si las columnas ya existen.

---

## ✅ Resumen de Cambios Realizados

### Archivos Modificados

#### Java JPA (Validación y Documentación)

1. **`src/main/java/com/devmatch/entity/Developer.java`**
   - ✅ Agregado import de `java.time.LocalDateTime`
   - ✅ Agregados 4 campos de auditoría
   - ✅ Agregados getters y setters para los campos de auditoría
   - ✅ Implementado método `onCreate()` con `@PrePersist`
   - ✅ Implementado método `onUpdate()` con `@PreUpdate`

2. **`src/main/java/com/devmatch/entity/Project.java`**
   - ✅ Agregado import de `java.time.LocalDateTime`
   - ✅ Agregados 4 campos de auditoría
   - ✅ Agregados getters y setters para los campos de auditoría
   - ✅ Implementado método `onCreate()` con `@PrePersist`
   - ✅ Implementado método `onUpdate()` con `@PreUpdate`

#### Python SQLAlchemy (Operaciones CRUD)

3. **`models.py`**
   - ✅ Agregados imports: `DateTime`, `event`, `datetime`, `os`
   - ✅ Agregados 4 campos de auditoría a `Developer`
   - ✅ Agregados 4 campos de auditoría a `Project`
   - ✅ Actualizado método `to_dict()` para incluir campos de auditoría
   - ✅ Implementado función `get_current_user()` para obtener usuario del sistema
   - ✅ Implementado evento `before_insert` para `Developer`
   - ✅ Implementado evento `before_update` para `Developer`
   - ✅ Implementado evento `before_insert` para `Project`
   - ✅ Implementado evento `before_update` para `Project`

### Líneas de Código Agregadas

- **Developer.java**: ~65 líneas (campos, getters/setters, callbacks)
- **Project.java**: ~65 líneas (campos, getters/setters, callbacks)
- **models.py**: ~70 líneas (campos, eventos, función auxiliar)
- **Total**: ~200 líneas de código relacionadas con auditoría

### Arquitectura Híbrida

La implementación en ambos sistemas garantiza:

1. **Coherencia**: Los mismos campos de auditoría en ambas capas
2. **Funcionalidad**: La auditoría funciona desde Python (donde se hacen las operaciones CRUD)
3. **Validación**: Las entidades JPA validan el esquema de la base de datos
4. **Documentación**: Las entidades Java documentan la estructura esperada

---

## 🎓 Conclusión

Esta implementación demuestra:

1. **Comprensión del concepto de auditoría**: Registro automático de quién y cuándo se realizan operaciones
2. **Buenas prácticas JPA y SQLAlchemy**: 
   - Uso de callbacks del ciclo de vida JPA (`@PrePersist`, `@PreUpdate`)
   - Uso de eventos SQLAlchemy (`before_insert`, `before_update`)
3. **Trazabilidad**: Campos que permiten rastrear el historial de cambios
4. **Automatización**: Los valores se mantienen actualizados sin intervención manual
5. **Arquitectura híbrida**: Implementación coherente en ambos sistemas (Java JPA y Python SQLAlchemy)

Los campos de auditoría están listos para ser utilizados y se actualizarán automáticamente cada vez que se cree o modifique un registro de `Developer` o `Project` en la base de datos, **tanto desde Java como desde Python**.

### Nota Importante sobre el Sistema Híbrido

Como DevMatch AI es un sistema híbrido:
- Las **operaciones CRUD reales** se realizan desde Python/Flask usando SQLAlchemy
- Los **eventos SQLAlchemy** son los que realmente se ejecutan en producción
- Las **entidades JPA Java** sirven para validación, documentación y cumplimiento de requisitos académicos
- Ambos sistemas mantienen la misma estructura de campos de auditoría para garantizar coherencia

---

**Fecha de Implementación**: 2025  
**Autor**: Caleb Nehemias  
**Proyecto**: DevMatch AI - Sistema de Matching Inteligente

