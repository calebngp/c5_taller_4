# ============================================================
# DevMatch AI - Integrado con DeepSeek para análisis semántico
# ============================================================

import json
import subprocess
from typing import Dict

# -------------------------------
# Datos precargados
# -------------------------------

proyectos = [
    {
        "id": 1,
        "nombre": "Sistema de pedidos para cafeterías",
        "descripcion": "Aplicación web para gestionar pedidos, menús y entregas en cafeterías. Buscamos personas que disfruten del trabajo colaborativo y de mejorar la experiencia del cliente.",
        "tecnologias_requeridas": ["Java", "Spring Boot", "PostgreSQL", "HTML", "CSS"],
        "nivel_experiencia": "Intermedio",
        "tipo_proyecto": "Web",
        "estado": "Abierto"
    },
    {
        "id": 2,
        "nombre": "App móvil de fitness con seguimiento de progreso",
        "descripcion": "Aplicación móvil para registrar rutinas de entrenamiento, motivar a los usuarios y ofrecer recomendaciones de salud basadas en datos.",
        "tecnologias_requeridas": ["Kotlin", "Firebase", "UI/UX"],
        "nivel_experiencia": "Avanzado",
        "tipo_proyecto": "Móvil",
        "estado": "Abierto"
    },
    {
        "id": 3,
        "nombre": "Plataforma de cursos online con pagos integrados",
        "descripcion": "Sitio para impartir cursos en video, con gestión de usuarios, sistema de pagos y análisis de progreso.",
        "tecnologias_requeridas": ["Python", "Django", "Stripe API", "JavaScript"],
        "nivel_experiencia": "Intermedio",
        "tipo_proyecto": "Web",
        "estado": "Abierto"
    }
]

desarrolladores = [
    {
        "id": 1,
        "nombre": "Ana López",
        "habilidades": ["Java", "Spring Boot", "PostgreSQL", "HTML"],
        "nivel_experiencia": "Intermedio",
        "motivacion": "Me gusta trabajar en proyectos donde se pueda impactar la experiencia del usuario. Me interesa crecer en arquitectura de software web.",
    },
    {
        "id": 2,
        "nombre": "Carlos Pérez",
        "habilidades": ["Kotlin", "Firebase", "UI/UX", "Java"],
        "nivel_experiencia": "Avanzado",
        "motivacion": "Apasionado por las apps móviles y la optimización de interfaces. Busco retos que involucren diseño y rendimiento.",
    },
    {
        "id": 3,
        "nombre": "Lucía Martínez",
        "habilidades": ["Python", "Django", "JavaScript", "React", "Stripe API"],
        "nivel_experiencia": "Intermedio",
        "motivacion": "Disfruto enseñar y aprender. Me encanta trabajar en proyectos educativos o de impacto social.",
    }
]

# -------------------------------
# Función de matching técnico
# -------------------------------

def calcular_match(proyecto: Dict, desarrollador: Dict) -> float:
    requeridas = set(proyecto["tecnologias_requeridas"])
    habilidades = set(desarrollador["habilidades"])
    coincidencias = requeridas & habilidades
    if not requeridas:
        return 0
    return (len(coincidencias) / len(requeridas)) * 100


# -------------------------------
# Integración con DeepSeek (Ollama)
# -------------------------------

def analizar_con_deepseek(proyecto: Dict, desarrollador: Dict) -> str:
    """Envía descripción y perfil a DeepSeek para análisis semántico."""
    prompt = f"""
Eres un asistente de emparejamiento inteligente.
Analiza si el siguiente desarrollador encaja en este proyecto y explica por qué.

Proyecto:
Nombre: {proyecto['nombre']}
Descripción: {proyecto['descripcion']}
Tecnologías requeridas: {', '.join(proyecto['tecnologias_requeridas'])}

Desarrollador:
Nombre: {desarrollador['nombre']}
Habilidades: {', '.join(desarrollador['habilidades'])}
Nivel de experiencia: {desarrollador['nivel_experiencia']}
Motivación: {desarrollador['motivacion']}

Evalúa afinidad técnica y afinidad motivacional (0 a 100) y da una breve explicación.
Responde en formato JSON:
{{"afinidad_tecnica": X, "afinidad_motivacional": Y, "comentario": "texto breve"}}
"""
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:1.5b"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode("utf-8").strip()

    # Intentar parsear JSON del modelo
    try:
        start = output.find("{")
        end = output.rfind("}") + 1
        parsed = json.loads(output[start:end])
        return parsed
    except Exception:
        return {"afinidad_tecnica": 0, "afinidad_motivacional": 0, "comentario": output}


# -------------------------------
# Mostrar resultados
# -------------------------------

def mostrar_resultados():
    print("\n=== RESULTADOS DE EMPAREJAMIENTO CON DEEPSEEK ===\n")
    for proyecto in proyectos:
        print(f"\nProyecto: {proyecto['nombre']}")
        print(f"Descripción: {proyecto['descripcion']}")
        print("------------------------------------------------")
        for dev in desarrolladores:
            score = calcular_match(proyecto, dev)
            analisis = analizar_con_deepseek(proyecto, dev)
            print(f"👤 {dev['nombre']}")
            print(f"  ▸ Coincidencia técnica: {score:.1f}%")
            print(f"  ▸ Afinidad técnica (IA): {analisis['afinidad_tecnica']}%")
            print(f"  ▸ Afinidad motivacional (IA): {analisis['afinidad_motivacional']}%")
            print(f"  💬 {analisis['comentario']}")
            print("------------------------------------------------")


# -------------------------------
# Ejecución
# -------------------------------

if __name__ == "__main__":
    mostrar_resultados()
