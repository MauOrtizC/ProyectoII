"#Visualizaci¢n de datos y mapas" 

from __future__ import annotations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


class Visualizador:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # --------- ESTÁTICOS (Matplotlib/Seaborn) ---------

    def histograma_popularidad(self):
        if "popularity" not in self.df.columns:
            return None, "No existe la columna popularity en el dataset."

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(self.df["popularity"].dropna(), bins=30)
        ax.set_title("¿La popularidad se concentra en pocas películas?")
        ax.set_xlabel("Popularidad")
        ax.set_ylabel("Frecuencia")

        p90 = self.df["popularity"].quantile(0.90)
        insight = (
            f"Insight: El 10% superior supera ~{p90:.2f} de popularidad, "
            "lo que sugiere una distribución sesgada donde pocas películas dominan la atención."
        )
        return fig, insight

    def scatter_budget_vs_revenue(self):
        if not {"budget", "revenue"}.issubset(self.df.columns):
            return None, "No existen budget y revenue; no se puede graficar rentabilidad."

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=self.df, x="budget", y="revenue", ax=ax, alpha=0.6)
        ax.set_title("¿Más presupuesto implica más ingresos? (budget vs revenue)")
        ax.set_xlabel("Budget")
        ax.set_ylabel("Revenue")

        corr = self.df[["budget", "revenue"]].corr(numeric_only=True).iloc[0, 1]
        insight = (
            f"Insight: La correlación budget–revenue es {corr:.2f}. "
            "Si es moderada/baja, indica que gastar más no garantiza recaudar más."
        )
        return fig, insight

    def heatmap_correlacion(self, corr: pd.DataFrame):
        if corr is None or corr.empty:
            return None, "No hay variables numéricas suficientes para correlación."

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=False, cmap="coolwarm", ax=ax)
        ax.set_title("Mapa de calor: relaciones entre variables numéricas")
        insight = (
            "Insight: Busca bloques rojos/azules fuertes: "
            "pueden sugerir variables redundantes o relaciones clave (ej. popularidad vs votos)."
        )
        return fig, insight

    # --------- INTERACTIVOS (Plotly) ---------

    def top_generos_bar(self):
        if "genres" not in self.df.columns:
            return None, "No existe genres normalizado."

        # genres es lista -> explotamos
        temp = self.df.dropna(subset=["genres"]).explode("genres")
        conteo = temp["genres"].value_counts().head(10).reset_index()
        conteo.columns = ["genre", "count"]

        fig = px.bar(conteo, x="genre", y="count",
                     title="Top 10 géneros más frecuentes (2020–2025)")
        insight = (
            "Insight: Los géneros dominantes reflejan tendencias del periodo. "
            "Úsalos como contexto para explicar qué tipo de contenido ‘gana’ en TMDB."
        )
        return fig, insight

    def tendencia_estrenos_por_anio(self):
        # intenta encontrar la columna fecha
        col_fecha = None
        for c in ["release_date", "releaseDate", "fecha_estreno"]:
            if c in self.df.columns:
                col_fecha = c
                break
        if col_fecha is None:
            return None, "No existe una columna de fecha de estreno."

        temp = self.df.dropna(subset=[col_fecha]).copy()
        temp["year"] = pd.to_datetime(temp[col_fecha], errors="coerce").dt.year
        conteo = temp["year"].value_counts().sort_index().reset_index()
        conteo.columns = ["year", "count"]

        fig = px.line(conteo, x="year", y="count", markers=True,
                      title="Evolución de estrenos por año (2020–2025)")
        insight = (
            "Insight: Picos o caídas pueden asociarse a eventos globales/industriales "
            "(ej. cambios de producción/estrenos), útil para narrativa del proyecto."
        )
        return fig, insight
