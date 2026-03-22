"#clase para dashboard" 

import streamlit as st
import pandas as pd
from src.eda.procesador_eda import ProcesadorEDA
from src.visualizacion.visualizador import Visualizador

st.set_page_config(page_title="TMDB Movie Insights", layout="wide")
st.title(" TMDB Movie Insights (2020–2025)")

df = pd.read_csv("data/processed/tmdb_movies_clean.csv")
viz = Visualizador(df)
eda = ProcesadorEDA(df)

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Películas", len(df))
c2.metric("% nulos (aprox.)", round(df.isna().sum().sum() / df.size * 100, 2))
if "vote_average" in df.columns:
    c3.metric("Promedio rating", round(df["vote_average"].mean(), 2))

st.divider()

# Gráfico 1
colA, colB = st.columns([2, 1])
fig1, insight1 = viz.top_generos_bar()
with colA:
    if fig1: st.plotly_chart(fig1, use_container_width=True)
with colB:
    st.subheader("Historia")
    st.write(insight1)

# Correlación
corr = eda.matriz_correlacion()
fig2, insight2 = viz.heatmap_correlacion(corr)
st.divider()
colC, colD = st.columns([2, 1])
with colC:
    if fig2: st.pyplot(fig2)
with colD:
    st.subheader("Historia")
    st.write(insight2)