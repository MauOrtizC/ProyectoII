# 🎬 TMDB Movie Insights

Proyecto de **Análisis Exploratorio de Datos (EDA)** y **Visualización Interactiva** utilizando un dataset de películas de **TMDB**.  
El objetivo es transformar datos crudos en **insights claros y accionables** mediante un pipeline reproducible y un **dashboard interactivo en Streamlit**.

📌 **Nota**: Este repositorio separa claramente la exploración (notebooks), la lógica final (código modular) y la presentación de resultados (dashboard).

---

## 🚀 Demo rápida

=======
# ProyectoII
Repositorio Proyecto II Programación II 
=======
## Mauricio Ortiz & Josué Redondo
# 🎬 TMDB Movie Insights

Proyecto de **Análisis Exploratorio de Datos (EDA)** y **Visualización Interactiva** utilizando un dataset de películas de **TMDB**. El objetivo es transformar datos crudos en **insights claros y accionables** mediante un pipeline reproducible y un **dashboard interactivo en Streamlit**.

---
## 🚀 Demo rápida
>>>>>>> 15ccbacb6c8bdd33a75dbb73d7772fe1d34720d5
```bash
# Ejecutar pipeline de datos
python -m src.main

# Ejecutar dashboard
streamlit run dashboard/app.py
<<<<<<< HEAD
```

Dashboard disponible en: `http://localhost:8501`

---

## 📁 Estructura del proyecto

```text
=======

## Estructura del Proyecto

>>>>>>> 15ccbacb6c8bdd33a75dbb73d7772fe1d34720d5
Movie_Insigths/
├── data/                 # Datos de entrada y salidas limpias
├── notebooks/            # Análisis exploratorio y justificación
├── src/                  # Pipeline y lógica final
│   ├── cargaDatos/
│   ├── helpers/
│   ├── eda/
│   └── visualizacion/
├── dashboard/            # Dashboard interactivo (Streamlit)
├── requirements.txt      # Dependencias del proyecto
└── README.md
<<<<<<< HEAD
```

---

## ⚙️ Requisitos

- **Python** 3.10 o superior  
- Librerías principales:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `streamlit`

Instalación de dependencias:

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Ejecución del proyecto

### 1️⃣ Pipeline de datos

```bash
python -m src.main
```

Este paso:
- Carga el dataset original  
- Limpia y normaliza columnas  
- Ejecuta el EDA final  
- Prepara los datos para visualización  

---

### 2️⃣ Dashboard interactivo

```bash
streamlit run dashboard/app.py
```

Permite explorar:
- Distribuciones de variables clave  
- Tendencias temporales  
- Comparaciones por métricas (popularidad, rating, etc.)  

---

## 📊 Resultados principales

- Dataset limpio y consistente  
- Visualizaciones claras y reutilizables  
- Insights sobre:
  - Popularidad de películas  
  - Comportamiento temporal  
  - Métricas de evaluación  

---

## 🧪 Notebooks (EDA)

Los notebooks se utilizan **exclusivamente para exploración, pruebas y documentación de decisiones**.

📌 **Importante**:
- La lógica validada en los notebooks se implementa posteriormente en `src/`
- Esto permite mantener un código limpio, modular y reproducible

Notebook principal:

```text
notebooks/01_EDA_TMDB.ipynb
```

---

## ✅ Buenas prácticas aplicadas

- Separación clara entre exploración y producción  
- Código modular y reutilizable  
- Pipeline reproducible  
- Dashboard desacoplado del backend  
- Compatibilidad con pandas 2.x  

---

## 👤 Autor

**Mauricio Ortiz**  
Proyecto académico / Data Analysis

---

⭐ *Si este proyecto te resulta útil o interesante, no dudes en darle una estrella al repositorio.*
=======
>>>>>>> 15ccbacb6c8bdd33a75dbb73d7772fe1d34720d5
