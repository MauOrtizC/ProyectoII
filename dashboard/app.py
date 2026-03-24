"#clase para dashboard" 

import streamlit as st
from eda.eda_utils import load_clean_data
from pca.pca_utils import run_pca

df = load_clean_data()

st.title("TMDB Movie Insights")

st.subheader("EDA")
st.dataframe(df.describe())

st.subheader("PCA")
pca_data = run_pca(df)
st.scatter_chart(pca_data)