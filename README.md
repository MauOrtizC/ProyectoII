# ProyectoII
Repositorio Proyecto II Programación II 
=======
## Mauricio Ortiz & Josué Redondo
# 🎬 TMDB Movie Insights

Proyecto de **Análisis Exploratorio de Datos (EDA)** y **Visualización Interactiva** utilizando un dataset de películas de **TMDB**. El objetivo es transformar datos crudos en **insights claros y accionables** mediante un pipeline reproducible y un **dashboard interactivo en Streamlit**.

---
## 🚀 Demo rápida
```bash
# Ejecutar pipeline de datos
python -m src.main

# Ejecutar dashboard
streamlit run dashboard/app.py

## Estructura del Proyecto

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
