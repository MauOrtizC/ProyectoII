"#clase para dashboard" 
import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# --- asegurar contexto del proyecto ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.eda.procesador_eda import ProcesadorEDA

# --- cargar dataset limpio ---
DATA_CLEAN = PROJECT_ROOT / "data" / "processed" / "tmdb_movies_clean.csv"
df = pd.read_csv(DATA_CLEAN)

eda = ProcesadorEDA(df)

st.title("TMDB Movie Insights")
st.subheader("Exploratory Data Analysis (EDA)")
st.subheader("Estudiantes: Mauricio Ortiz & Josué Redondo")

# ==========================================================
# 1️⃣ Vista general (igual al notebook)
# ==========================================================
st.header("Vista general del dataset")
st.write(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
st.dataframe(df.head())

# ==========================================================
# 2️⃣ Estadísticas descriptivas
# ==========================================================
st.header("Estadísticas descriptivas")
st.dataframe(eda.resumen_descriptivo())

# ==========================================================
# 3️⃣ Distribuciones (Histogramas / Boxplots)
# ==========================================================
st.header("Distribución de variables numéricas")

num_cols = df.select_dtypes(include="number").columns.tolist()
col = st.selectbox("Selecciona una variable numérica", num_cols)

fig, ax = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(df[col], kde=True, ax=ax[0])
ax[0].set_title(f"Histograma de {col}")

sns.boxplot(x=df[col], ax=ax[1])
ax[1].set_title(f"Boxplot de {col}")

st.pyplot(fig)

# ==========================================================
# 4️⃣ Matriz de correlación
# ==========================================================
st.header("Matriz de correlación")

corr = eda.matriz_correlacion()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# ==========================================================
# 5️⃣ Outliers (IQR)
# ==========================================================
st.header("Detección de outliers (IQR)")

col_outlier = st.selectbox("Variable para detectar outliers", num_cols, key="outliers")
outliers = eda.detectar_outliers_iqr(col_outlier)

st.write(f"Outliers detectados: {len(outliers)}")
st.dataframe(outliers.head())


