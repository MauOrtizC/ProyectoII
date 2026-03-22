"#Exploraci¢n de Datos y Estad¡sticas Descriptivas" 

from __future__ import annotations
import pandas as pd
import numpy as np
from src.helpers.utilidades import Utilidades


class ProcesadorEDA:
    """
    - Limpieza de datos
    - Resumen descriptivo
    - Matriz de correlación
    - Extras: outliers y rentabilidad (si existen columnas budget/revenue)
    """

    def __init__(self, df: pd.DataFrame):
        self.df_original = df.copy()
        self.df = df.copy()

    def limpieza_datos(self) -> pd.DataFrame:
        df = self.df

        # 1) Eliminar duplicados
        df = df.drop_duplicates()

        # 2) Tipos: fecha (si existe)
        for col_fecha in ["release_date", "releaseDate", "fecha_estreno"]:
            if col_fecha in df.columns:
                df[col_fecha] = Utilidades.parse_fecha(df[col_fecha])

        # 3) Normalización de idiomas (si existe)
        for col_lang in ["original_language", "originalLanguage", "language"]:
            if col_lang in df.columns:
                df[col_lang] = Utilidades.normalizar_idioma(df[col_lang])

        # 4) Normalización de géneros (si existe)
        for col_gen in ["genres", "genre", "genres_list"]:
            if col_gen in df.columns:
                df[col_gen] = Utilidades.normalizar_generos(df[col_gen])

        # 5) Conversión de numéricos típicos (si existen)
        numericas_posibles = [
            "budget", "revenue", "popularity", "vote_average", "vote_count", "runtime"
        ]
        for c in Utilidades.asegurar_columnas(df, numericas_posibles):
            df[c] = pd.to_numeric(df[c], errors="coerce")

        # 6) Manejo de nulos (justificado)
        #    - Si faltan campos críticos como título, eliminamos (no se puede analizar)
        for col_titulo in ["title", "original_title", "name"]:
            if col_titulo in df.columns:
                df = df.dropna(subset=[col_titulo])
                break

        #    - Para numéricos: imputación con mediana (robusta)
        for c in Utilidades.asegurar_columnas(df, numericas_posibles):
            if df[c].isna().any():
                med = df[c].median()
                df[c] = df[c].fillna(med)

        #    - Para categóricos: imputación con "unknown"
        categoricas_posibles = ["original_language", "status"]
        for c in Utilidades.asegurar_columnas(df, categoricas_posibles):
            df[c] = df[c].fillna("unknown")

        # 7) Feature engineering útil
        if "revenue" in df.columns and "budget" in df.columns:
            df["profit"] = df["revenue"] - df["budget"]
            # evitar división por 0
            df["roi"] = np.where(df["budget"] > 0, df["profit"] / df["budget"], np.nan)

        self.df = df
        return df

    def guardar_limpio(self, ruta_salida: str) -> None:
        self.df.to_csv(ruta_salida, index=False)

    def resumen_descriptivo(self) -> pd.DataFrame:
        """
        Medidas: count, mean, std, min, q1, median, q3, max para variables numéricas.
        """
        num = self.df.select_dtypes(include=[np.number])
        if num.shape[1] == 0:
            return pd.DataFrame()

        resumen = num.describe(percentiles=[0.25, 0.5, 0.75]).T
        resumen = resumen.rename(
            columns={"25%": "q1", "50%": "median", "75%": "q3"}
        )
        # garantizar orden solicitado
        orden = ["count", "mean", "std", "min", "q1", "median", "q3", "max"]
        resumen = resumen[orden]
        return resumen

    def matriz_correlacion(self) -> pd.DataFrame:
        num = self.df.select_dtypes(include=[np.number])
        if num.shape[1] == 0:
            return pd.DataFrame()
        return num.corr(numeric_only=True)

    def detectar_outliers_iqr(self, columna: str) -> pd.DataFrame:
        """
        Devuelve filas consideradas outliers usando método IQR.
        """
        if columna not in self.df.columns:
            raise ValueError(f"No existe la columna: {columna}")

        s = self.df[columna].dropna()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        lo = q1 - 1.5 * iqr
        hi = q3 + 1.5 * iqr
        return self.df[(self.df[columna] < lo) | (self.df[columna] > hi)]

    def top_rentables(self, n: int = 10) -> pd.DataFrame:
        """
        Top películas por ROI (si existe).
        """
        if "roi" not in self.df.columns:
            return pd.DataFrame()
        cols = [c for c in ["title", "revenue", "budget", "profit", "roi"] if c in self.df.columns]
        return self.df.dropna(subset=["roi"]).sort_values("roi", ascending=False)[cols].head(n)
