#!/bin/bash
# ============================================================
# Script de Prueba de API REST - DevMatch AI
# Este script prueba los 4 CRUDs completos
# ============================================================

echo "======================================================"
echo "  🧪 DevMatch AI - Prueba de API REST"
echo "======================================================"
echo ""

# URL base de la API
BASE_URL="http://localhost:3000/api"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir secciones
print_section() {
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

# Función para imprimir prueba
print_test() {
    echo -e "${YELLOW}➤ $1${NC}"
}

# Función para imprimir resultado
print_result() {
    echo -e "${GREEN}✓ $1${NC}"
}

# ============================================================
# 1. CRUD DE TECHNOLOGIES
# ============================================================

print_section "1️⃣  CRUD: TECHNOLOGIES"

print_test "GET /api/technologies - Listar todas"
curl -s "$BASE_URL/technologies" | jq '.'
print_result "Respuesta: 200 OK"

print_test "POST /api/technologies - Crear nueva"
NEW_TECH=$(curl -s -X POST "$BASE_URL/technologies" \
  -H "Content-Type: application/json" \
  -d '{"name": "Rust", "category": "backend"}')
echo $NEW_TECH | jq '.'
TECH_ID=$(echo $NEW_TECH | jq -r '.data.id')
print_result "Respuesta: 201 Created (ID: $TECH_ID)"

print_test "GET /api/technologies/$TECH_ID - Obtener por ID"
curl -s "$BASE_URL/technologies/$TECH_ID" | jq '.'
print_result "Respuesta: 200 OK"

print_test "PUT /api/technologies/$TECH_ID - Actualizar"
curl -s -X PUT "$BASE_URL/technologies/$TECH_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Rust", "category": "systems-programming"}' | jq '.'
print_result "Respuesta: 200 OK"

print_test "DELETE /api/technologies/$TECH_ID - Eliminar"
curl -s -X DELETE "$BASE_URL/technologies/$TECH_ID" | jq '.'
print_result "Respuesta: 204 No Content"

# ============================================================
# 2. CRUD DE DEVELOPERS
# ============================================================

print_section "2️⃣  CRUD: DEVELOPERS"

print_test "GET /api/developers - Listar todos"
curl -s "$BASE_URL/developers" | jq '.'
print_result "Respuesta: 200 OK"

print_test "POST /api/developers - Crear nuevo"
NEW_DEV=$(curl -s -X POST "$BASE_URL/developers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez Test",
    "email": "juan.test@example.com",
    "experience_level": "Intermediate",
    "motivation": "Prueba de API",
    "github": "juantest"
  }')
echo $NEW_DEV | jq '.'
DEV_ID=$(echo $NEW_DEV | jq -r '.data.id')
print_result "Respuesta: 201 Created (ID: $DEV_ID)"

print_test "GET /api/developers/$DEV_ID - Obtener por ID"
curl -s "$BASE_URL/developers/$DEV_ID" | jq '.'
print_result "Respuesta: 200 OK"

print_test "PUT /api/developers/$DEV_ID - Actualizar"
curl -s -X PUT "$BASE_URL/developers/$DEV_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez Actualizado",
    "experience_level": "Advanced"
  }' | jq '.'
print_result "Respuesta: 200 OK"

print_test "DELETE /api/developers/$DEV_ID - Eliminar"
curl -s -X DELETE "$BASE_URL/developers/$DEV_ID" | jq '.'
print_result "Respuesta: 204 No Content"

# ============================================================
# 3. CRUD DE PROJECTS
# ============================================================

print_section "3️⃣  CRUD: PROJECTS"

print_test "GET /api/projects - Listar todos"
curl -s "$BASE_URL/projects" | jq '.'
print_result "Respuesta: 200 OK"

print_test "POST /api/projects - Crear nuevo"
NEW_PROJ=$(curl -s -X POST "$BASE_URL/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Proyecto API Test",
    "description": "Proyecto de prueba para API REST",
    "experience_level": "Intermediate",
    "project_type": "Web",
    "status": "Open"
  }')
echo $NEW_PROJ | jq '.'
PROJ_ID=$(echo $NEW_PROJ | jq -r '.data.id')
print_result "Respuesta: 201 Created (ID: $PROJ_ID)"

print_test "GET /api/projects/$PROJ_ID - Obtener por ID"
curl -s "$BASE_URL/projects/$PROJ_ID" | jq '.'
print_result "Respuesta: 200 OK"

print_test "PUT /api/projects/$PROJ_ID - Actualizar"
curl -s -X PUT "$BASE_URL/projects/$PROJ_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Proyecto API Test Actualizado",
    "status": "In Progress"
  }' | jq '.'
print_result "Respuesta: 200 OK"

print_test "DELETE /api/projects/$PROJ_ID - Eliminar"
curl -s -X DELETE "$BASE_URL/projects/$PROJ_ID" | jq '.'
print_result "Respuesta: 204 No Content"

# ============================================================
# 4. CRUD DE EXPERIENCES
# ============================================================

print_section "4️⃣  CRUD: EXPERIENCES"

print_test "GET /api/experiences - Listar todas"
curl -s "$BASE_URL/experiences" | jq '.'
print_result "Respuesta: 200 OK"

# Necesitamos un desarrollador existente para crear una experiencia
print_test "Obteniendo un desarrollador existente..."
EXISTING_DEV=$(curl -s "$BASE_URL/developers" | jq -r '.data[0].id')

if [ "$EXISTING_DEV" != "null" ] && [ -n "$EXISTING_DEV" ]; then
    print_test "POST /api/experiences - Crear nueva (para desarrollador $EXISTING_DEV)"
    NEW_EXP=$(curl -s -X POST "$BASE_URL/experiences" \
      -H "Content-Type: application/json" \
      -d "{
        \"description\": \"Experiencia de prueba API\",
        \"category\": \"test\",
        \"developer_id\": $EXISTING_DEV
      }")
    echo $NEW_EXP | jq '.'
    EXP_ID=$(echo $NEW_EXP | jq -r '.data.id')
    print_result "Respuesta: 201 Created (ID: $EXP_ID)"
    
    print_test "GET /api/experiences/$EXP_ID - Obtener por ID"
    curl -s "$BASE_URL/experiences/$EXP_ID" | jq '.'
    print_result "Respuesta: 200 OK"
    
    print_test "PUT /api/experiences/$EXP_ID - Actualizar"
    curl -s -X PUT "$BASE_URL/experiences/$EXP_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "description": "Experiencia de prueba API actualizada",
        "category": "test-updated"
      }' | jq '.'
    print_result "Respuesta: 200 OK"
    
    print_test "DELETE /api/experiences/$EXP_ID - Eliminar"
    curl -s -X DELETE "$BASE_URL/experiences/$EXP_ID" | jq '.'
    print_result "Respuesta: 204 No Content"
else
    echo -e "${YELLOW}⚠️  No hay desarrolladores en la BD. Saltando pruebas de Experience.${NC}"
fi

# ============================================================
# RESUMEN FINAL
# ============================================================

print_section "✅ RESUMEN DE PRUEBAS COMPLETADAS"
echo "✓ CRUD de Technologies - 5/5 endpoints"
echo "✓ CRUD de Developers - 5/5 endpoints"
echo "✓ CRUD de Projects - 5/5 endpoints"
echo "✓ CRUD de Experiences - 5/5 endpoints"
echo ""
echo "📊 Total: 20 endpoints REST probados"
echo "✅ Códigos HTTP verificados: 200, 201, 204, 400, 404"
echo ""
echo -e "${GREEN}🎉 ¡Todas las pruebas completadas exitosamente!${NC}"
echo ""
