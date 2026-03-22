"#Funciones auxiliares reutilizables"


from __future__ import annotations
import ast
import re
from typing import Any, Optional, List
import pandas as pd


class Utilidades:
    @staticmethod
    def porcentaje_nulos(df: pd.DataFrame) -> float:
        """Retorna el porcentaje total de valores nulos en el DataFrame."""
        total = df.size
        if total == 0:
            return 0.0
        return round((df.isna().sum().sum() / total) * 100, 2)

    @staticmethod
    def parse_fecha(col: pd.Series) -> pd.Series:
        """Convierte una columna a datetime (si se puede)."""
        return pd.to_datetime(col, errors="coerce")

    @staticmethod
    def normalizar_idioma(col: pd.Series) -> pd.Series:
        """Normaliza idiomas tipo 'EN', 'en ', 'English' a un formato estable (minúsculas ISO-like)."""
        def norm(x: Any) -> Any:
            if pd.isna(x):
                return x
            s = str(x).strip().lower()
            # mapeos comunes opcionales
            mapa = {"english": "en", "spanish": "es", "french": "fr"}
            return mapa.get(s, s)
        return col.apply(norm)

    @staticmethod
    def normalizar_generos(col: pd.Series) -> pd.Series:
        """
        Normaliza géneros a una lista de strings.
        Soporta formatos típicos: 'Action|Drama', '["Action","Drama"]', "[{'id': 28, 'name':'Action'}]".
        """
        def to_list(x: Any) -> Optional[List[str]]:
            if pd.isna(x):
                return None
            s = str(x).strip()

            # Caso: separados por | o coma
            if "|" in s:
                parts = [p.strip() for p in s.split("|") if p.strip()]
                return parts if parts else None

            # Caso: lista serializada
            try:
                obj = ast.literal_eval(s)
                if isinstance(obj, list):
                    # lista de strings
                    if all(isinstance(i, str) for i in obj):
                        return [i.strip() for i in obj if i.strip()]
                    # lista de dicts con name
                    if all(isinstance(i, dict) for i in obj):
                        names = []
                        for d in obj:
                            if "name" in d and d["name"]:
                                names.append(str(d["name"]).strip())
                        return names if names else None
            except Exception:
                pass

            # Caso: string simple
            s = re.sub(r"\s+", " ", s)
            return [s] if s else None

        return col.apply(to_list)

    @staticmethod
    def asegurar_columnas(df: pd.DataFrame, cols: list[str]) -> list[str]:
        """Devuelve cuáles columnas existen dentro de df (evita errores si el dataset cambia)."""
        return [c for c in cols if c in df.columns]
