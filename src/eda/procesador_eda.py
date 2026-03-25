# Exploración de Datos y Estadísticas Descriptivas

from __future__ import annotations
import pandas as pd
import numpy as np
from src.helpers.utilidades import Utilidades


class ProcesadorEDA:

    def __init__(self, df: pd.DataFrame):
        self.df_original = df.copy()
        self.df = df.copy()

    def limpieza_datos(self) -> pd.DataFrame:
        df = self.df

        # 0) Eliminar columnas no analíticas (rutas de imágenes)
        columnas_no_utiles = ["poster_path", "backdrop_path"]
        df = df.drop(
            columns=[c for c in columnas_no_utiles if c in df.columns],
            errors="ignore"
        )

        # 1) Eliminar duplicados
        df = df.drop_duplicates()

        # 2) Conversión de fechas (si existen)
        for col_fecha in ["release_date", "releaseDate", "fecha_estreno"]:
            if col_fecha in df.columns:
                df[col_fecha] = Utilidades.parse_fecha(df[col_fecha])


        # 3) Conversión de columnas numéricas típicas
        numericas_posibles = [
            "budget",
            "revenue",
            "popularity",
            "vote_average",
            "vote_count",
            "runtime",
        ]

        for c in Utilidades.asegurar_columnas(df, numericas_posibles):
            df[c] = pd.to_numeric(df[c], errors="coerce")

        #  Manejo de valores nulos
        #  Eliminar filas sin título
        for col_titulo in ["title", "original_title", "name"]:
            if col_titulo in df.columns:
                df = df.dropna(subset=[col_titulo])
                break

        # Numéricos → imputación con mediana
        for c in Utilidades.asegurar_columnas(df, numericas_posibles):
            if df[c].isna().any():
                df[c] = df[c].fillna(df[c].median())

        # Categóricos → "unknown"
        categoricas_posibles = ["original_language", "status"]
        for c in Utilidades.asegurar_columnas(df, categoricas_posibles):
            df[c] = df[c].fillna("unknown")

        #
        if "revenue" in df.columns and "budget" in df.columns:
            df["profit"] = df["revenue"] - df["budget"]
            df["roi"] = np.where(
                df["budget"] > 0,
                df["profit"] / df["budget"],
                np.nan
            )

        self.df = df
        return df

    def guardar_limpio(self, ruta_salida: str) -> None:
        """
        Guarda el DataFrame limpio en CSV.
        Nota: asegúrate de que el archivo no esté abierto en Excel.
        """
        self.df.to_csv(ruta_salida, index=False)


    def resumen_descriptivo(self) -> pd.DataFrame:

        num = self.df.select_dtypes(include=[np.number])
        if num.empty:
            return pd.DataFrame()

        resumen = num.describe(percentiles=[0.25, 0.5, 0.75]).T
        resumen = resumen.rename(
            columns={"25%": "q1", "50%": "median", "75%": "q3"}
        )

        orden = ["count", "mean", "std", "min", "q1", "median", "q3", "max"]
        return resumen[orden]

    def matriz_correlacion(self) -> pd.DataFrame:

        num = self.df.select_dtypes(include=[np.number])
        if num.empty:
            return pd.DataFrame()
        return num.corr(numeric_only=True)

    def detectar_outliers_iqr(self, columna: str) -> pd.DataFrame:

        if columna not in self.df.columns:
            raise ValueError(f"No existe la columna: {columna}")

        s = self.df[columna].dropna()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1

        limite_inf = q1 - 1.5 * iqr
        limite_sup = q3 + 1.5 * iqr

        return self.df[
            (self.df[columna] < limite_inf) |
            (self.df[columna] > limite_sup)
        ]

    def top_rentables(self, n: int = 10) -> pd.DataFrame:
     
        if "roi" not in self.df.columns:
            return pd.DataFrame()

        columnas = [
            c for c in ["title", "revenue", "budget", "profit", "roi"]
            if c in self.df.columns
        ]

        return (
            self.df
            .dropna(subset=["roi"])
            .sort_values("roi", ascending=False)[columnas]
            .head(n)
        )