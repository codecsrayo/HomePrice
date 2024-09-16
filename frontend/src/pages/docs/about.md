<a href="/">Inicio</a>
<a href="/panel">Probar</a>


# Diseño e Implementación del Proyecto
---
### Elaborado por
**Brayan Andrés Rayo Quintero**

### Ficha
PREICA2402B010061

### Asignatura
Proyecto Integrado I - Desarrollo de Aplicaciones

### Profesor
Julio Cesar Martinez

### Institución
Institución Universitaria Digital de Antioquia  
Medellín, 08 de septiembre del 2024

---

## Resumen
Este proyecto consiste en la implementación de un modelo de machine learning con el objetivo de predecir los precios de viviendas. Está desarrollado en una arquitectura de microservicios basada en contenedores Docker, siguiendo el estándar REST.  
Tecnologías utilizadas:  
- Backend: Python (FastAPI)
- Frontend: Typescript (Astro)
- Base de datos: PostgreSQL



## Introducción
HomePrice es una aplicación web innovadora diseñada para predecir los precios de las viviendas utilizando técnicas avanzadas de aprendizaje automático. Se implementa un modelo de regresión basado en características clave de las propiedades para proporcionar estimaciones precisas del valor de mercado. Utiliza la metodología ágil Scrum y herramientas como Python, FastAPI, y sklearn para ofrecer una solución robusta y escalable.



## Descripción
HomePrice es una aplicación web que utiliza un modelo de regresión para estimar los precios de las viviendas basado en diversas características de las propiedades.



## Fundamentos Teóricos
1. Regresión Lineal Múltiple: Técnica estadística que modela la relación entre múltiples variables independientes y una dependiente.
2. Preprocesamiento de Datos: Incluye limpieza, manejo de valores faltantes, codificación de variables categóricas y normalización.
3. Validación Cruzada: Método para evaluar la capacidad de generalización del modelo.
4. Métricas de Evaluación: Se utilizan MSE y R² para medir el rendimiento del modelo.



## Resolución del Problema
El proyecto resuelve la problemática de la estimación de precios de vivienda mediante un modelo de aprendizaje automático que facilita la toma de decisiones en el mercado inmobiliario.



## Tecnologías y Herramientas
- Backend: Python (FastAPI)
- **Frontend: Astro (Typescript)
- Modelo ML: scikit-learn y TensorFlow
- Base de Datos: PostgreSQL



## Alcance del Proyecto
1. Desarrollo del modelo de predicción.
2. Implementación de la interfaz de usuario.
3. Integración del backend con el frontend.
4. Despliegue de la aplicación en un entorno de prueba.



## Problemática Social a Abordar
1. Mejorar la planificación urbana.
2. Facilitar el acceso a viviendas asequibles.
3. Promover la transparencia en el mercado inmobiliario.

---

## Cronograma


| Semana | Actividad | Responsable | Fecha Inicio | Fecha Fin |
|--------|-----------|-------------|--------------|-----------|
| 1 | Análisis de requisitos y diseño inicial | Equipo completo | 2024-09-08 | 2024-09-10 |
| 2 | Configuración del entorno de desarrollo | Desarrollador Backend | 2024-09-08 | 2024-09-10 |
| 2 | Diseño de la interfaz de usuario | Diseñador UX/UI | 2024-09-08 | 2024-09-15 |
| 3 | Desarrollo del modelo ML básico | Científico de Datos | - | - |
| 4 | Implementación del backend (API) | Desarrollador Backend | - | - |
| 5 | Desarrollo del frontend | Desarrollador Frontend | - | - |
| 6 | Integración y pruebas unitarias | Equipo completo | - | - |
| 7 | Pruebas de integración y depuración | Tester | - | - |
| 8 | Documentación y preparación para el despliegue | Equipo completo | - | - |

---

## Organización del Proyecto
Para la gestión eficiente del proyecto HomePrice, se ha implementado una estructura organizativa basada en los principios de Scrum.



## Arquitectura
1. Cliente Web (Frontend): Desarrollado en Astro, se comunica con el backend a través de API RESTful.
2. Servicio de Predicción: Contiene el modelo de ML para la predicción de precios, implementado con FastAPI y scikit-learn.
3. Servicio de Gestión de Datos: Maneja las operaciones CRUD para los datos de propiedades, usando PostgreSQL.
4. Base de Datos: PostgreSQL para almacenamiento persistente.



## Prototipo, Wireframe o Mockups

Formulario del modelo:
[Imagen o descripción del formulario]  
Respuesta del modelo: 
[Imagen o descripción de la respuesta]



## Modelo Entidad Relación
El modelo de datos de HomePrice incluye las siguientes entidades:
1. properties: Información básica de las propiedades.
2. features: Características adicionales de las propiedades.
3. predictions: Predicciones de precios.
4. models: Información sobre los modelos de aprendizaje.
5. model_predictions: Relación entre modelos y predicciones.



## Conclusiones
La implementación de técnicas de aprendizaje automático para la predicción de precios inmobiliarios es una herramienta valiosa para el mercado inmobiliario.



## Referencias
1. Fan, C., Cui, Z., & Zhong, X. (2018). House prices prediction with machine learning algorithms.
2. Park, B., & Bae, J. K. (2015). Using machine learning algorithms for housing price prediction.
3. Pow, N., Janulewicz, E., & Liu, L. (2014). Applied machine learning project.

<a href="/">Inicio</a>
<a href="/panel">Probar</a>

<style>
  * {
    margin: 30px;
    color: white;
    background: #242424;
  }
     a {
        padding: 4px;
        text-decoration: none;
        color: white;
        font-size: 15px;
        font-family: sans-serif;
    }

    a:focus,
    a:hover {
        border-bottom: 1px solid;
        opacity: 80%;
    }
    table{
        background: white;
    }

</style>