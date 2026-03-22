"# Punto de entrada del proyecto"

from src.cargaDatos.cargador_datos import CargadorDatos
from src.eda.procesador_eda import ProcesadorEDA
from src.visualizacion.visualizador import Visualizador

DATA_RAW = "data/raw/tmdb_2020_to_2025.csv"
DATA_CLEAN = "data/processed/tmdb_movies_clean.csv"

def main():
    # 1) Carga
    loader = CargadorDatos(DATA_RAW)
    df = loader.cargar()
    resumen = loader.resumen_carga()
    print(f"[Carga] Filas: {resumen.filas} | Columnas: {resumen.columnas} | %Nulos: {resumen.porcentaje_nulos}")

    # 2) EDA / Limpieza
    eda = ProcesadorEDA(df)
    df_clean = eda.limpieza_datos()
    eda.guardar_limpio(DATA_CLEAN)
    print(f"[EDA] Dataset limpio guardado en: {DATA_CLEAN}")

    # 3) Resumen descriptivo
    desc = eda.resumen_descriptivo()
    if not desc.empty:
        print("\n[Resumen descriptivo]\n", desc.head())

    # 4) Correlación
    corr = eda.matriz_correlacion()
    if not corr.empty:
        print("\n[Correlación] OK")

    # 5) Visualización básica (ejemplo)
    viz = Visualizador(df_clean)
    fig, insight = viz.histograma_popularidad()
    if fig:
        print("\n[Insight]", insight)
        fig.show()

if __name__ == "__main__":
    main()
