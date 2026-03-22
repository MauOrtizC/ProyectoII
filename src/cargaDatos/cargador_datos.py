"#clase para cargar datos"

from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
from src.helpers.utilidades import Utilidades


@dataclass
class ResultadoCarga:
    filas: int
    columnas: int
    porcentaje_nulos: float


class CargadorDatos:
    """
    Carga el dataset desde data/raw/tmdb_2020_to_2025.csv
    y registra: número de filas y % de nulos.
    """

    def __init__(self, ruta_csv: str):
        self.ruta_csv = ruta_csv
        self.df: pd.DataFrame | None = None
        self.resultado: ResultadoCarga | None = None

    def cargar(self, encoding: str = "utf-8") -> pd.DataFrame:
        try:
            df = pd.read_csv(self.ruta_csv, encoding=encoding)
        except UnicodeDecodeError:
            # fallback típico
            df = pd.read_csv(self.ruta_csv, encoding="latin-1")

        self.df = df
        self.resultado = ResultadoCarga(
            filas=df.shape[0],
            columnas=df.shape[1],
            porcentaje_nulos=Utilidades.porcentaje_nulos(df),
        )
        return df

    def resumen_carga(self) -> ResultadoCarga:
        if self.resultado is None:
            raise ValueError("Primero debes ejecutar cargar().")
        return self.resultado
