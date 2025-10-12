#!/bin/bash

# Script para compilar y ejecutar el launcher Java
# DevMatch AI - Java Launcher

echo "🔧 Compilando PythonServerLauncher.java..."

# Verificar que Java esté instalado
if ! command -v javac &> /dev/null; then
    echo "❌ Error: javac no está instalado. Instala Java JDK primero."
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo "❌ Error: java no está instalado. Instala Java JRE primero."
    exit 1
fi

# Compilar el archivo Java
javac PythonServerLauncher.java

if [ $? -eq 0 ]; then
    echo "✅ Compilación exitosa!"
    echo "🚀 Ejecutando launcher..."
    echo ""
    
    # Ejecutar el programa Java
    java PythonServerLauncher
else
    echo "❌ Error en la compilación"
    exit 1
fi