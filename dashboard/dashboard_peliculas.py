# ============================================
# DASHBOARD DE PELÍCULAS - STREAMLIT
# Proyecto estudiantil con POO básica
# ============================================

# IMPORTACIONES
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================
# CLASE PRINCIPAL: AnalizadorPeliculas
# ============================================
class AnalizadorPeliculas:
    """
    Clase que encapsula toda la lógica de análisis de películas.
    
    ¿Qué es una clase?
    - Es como un "molde" o "plantilla" para crear objetos
    - Agrupa datos (atributos) y funciones (métodos) relacionados
    
    Atributos (datos que guarda):
    - df: El DataFrame con todas las películas
    
    Métodos (funciones que puede hacer):
    - cargar_datos(): Lee el archivo CSV
    - calcular_metricas(): Calcula estadísticas generales
    - grafico_XXX(): Crea cada gráfico
    """
    
    def __init__(self, ruta_archivo):
        """
        Constructor de la clase.
        
        ¿Qué es __init__?
        - Es el método "constructor", se ejecuta al crear el objeto
        - Inicializa los atributos (variables) del objeto
        - self = referencia al objeto mismo
        
        Parámetros:
        - ruta_archivo: Ubicación del CSV
        """
        # Ruta de la PC de Josué
        self.ruta_archivo = r"C:\Movie_Insigths\data\processed\tmdb_movies_clean.csv"
        self.df = None  # Inicialmente vacío
    
    def cargar_datos(self):
        """
        Carga el archivo CSV en un DataFrame.
        
        ¿Por qué un método separado?
        - Separación de responsabilidades (buen POO)
        - Puedo reutilizarlo
        - Fácil de modificar o debuggear
        
        Returns:
        - bool: True si cargó bien, False si hubo error
        """
        try:
            # Leer CSV
            self.df = pd.read_csv(self.ruta_archivo)
            
            # Convertir fecha a formato datetime (para poder trabajar con años)
            self.df['release_date'] = pd.to_datetime(self.df['release_date'], errors='coerce')
            
            # Extraer el año en una nueva columna
            self.df['year'] = self.df['release_date'].dt.year
            
            return True
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            return False
    
    def calcular_metricas(self):
        """
        Calcula las métricas principales del dataset.
        
        Returns:
        - dict: Diccionario con las métricas
        """
        metricas = {
            'total_peliculas': len(self.df),
            'calificacion_promedio': self.df['vote_average'].mean(),
            'total_idiomas': self.df['original_language'].nunique(),
            'anio_minimo': int(self.df['year'].min()) if self.df['year'].notna().any() else 0,
            'anio_maximo': int(self.df['year'].max()) if self.df['year'].notna().any() else 0
        }
        return metricas
    
    def grafico_distribucion_calificaciones(self):
        """
        Crea histograma de distribución de calificaciones.
        
        ¿Qué muestra?
        - Cuántas películas tienen cada rango de calificación
        - Si la mayoría son buenas, malas o mediocres
        
        Returns:
        - plotly figure object
        """
        fig = px.histogram(
            self.df,
            x='vote_average',
            nbins=20,  # 20 "barras" en el histograma
            title='Distribución de Calificaciones',
            labels={'vote_average': 'Calificación', 'count': 'Cantidad de Películas'},
            color_discrete_sequence=['#1f77b4']  # Color azul
        )
        
        # Personalización
        fig.update_layout(
            xaxis_title='Calificación (0-10)',
            yaxis_title='Número de Películas',
            showlegend=False
        )
        
        return fig
    
    def grafico_top_idiomas(self, top_n=10):
        """
        Crea gráfico de barras con los idiomas más comunes.
        
        ¿Qué muestra?
        - Qué idiomas tienen más películas
        - Dominancia de ciertas industrias (Hollywood, Bollywood, etc.)
        
        Parámetros:
        - top_n: Cuántos idiomas mostrar (default: 10)
        
        Returns:
        - plotly figure object
        """
        # Contar películas por idioma
        conteo_idiomas = self.df['original_language'].value_counts().head(top_n)
        
        # Crear gráfico de barras horizontal
        fig = go.Figure(data=[
            go.Bar(
                y=conteo_idiomas.index,  # Idiomas en el eje Y
                x=conteo_idiomas.values,  # Cantidades en el eje X
                orientation='h',  # Horizontal
                marker_color='lightseagreen'
            )
        ])
        
        fig.update_layout(
            title=f'Top {top_n} Idiomas Más Comunes',
            xaxis_title='Número de Películas',
            yaxis_title='Idioma',
            yaxis={'categoryorder': 'total ascending'}  # Ordenar de menor a mayor
        )
        
        return fig
    
    def grafico_evolucion_temporal(self):
        """
        Crea gráfico de línea mostrando películas por año.
        
        ¿Qué muestra?
        - Cómo ha cambiado la producción cinematográfica a lo largo del tiempo
        - Épocas doradas del cine
        - Boom reciente de producción
        
        Returns:
        - plotly figure object
        """
        # Filtrar años válidos (no NaN)
        df_con_anio = self.df[self.df['year'].notna()].copy()
        
        # Contar películas por año
        peliculas_por_anio = df_con_anio.groupby('year').size().reset_index(name='cantidad')
        
        # Crear gráfico de línea
        fig = px.line(
            peliculas_por_anio,
            x='year',
            y='cantidad',
            title='Evolución de la Producción Cinematográfica',
            labels={'year': 'Año', 'cantidad': 'Número de Películas'}
        )
        
        # Personalización
        fig.update_traces(line_color='#ff7f0e', line_width=2)
        fig.update_layout(
            xaxis_title='Año',
            yaxis_title='Películas Producidas',
            hovermode='x unified'
        )
        
        return fig
    
    def grafico_popularidad_vs_calificacion(self):
        """
        Crea scatter plot de Popularidad vs Calificación.
        
        ¿Qué muestra?
        - Si las películas populares son realmente buenas
        - Identifica joyas ocultas y películas sobrevaloradas
        - Cada punto = una película
        
        Returns:
        - plotly figure object
        """
        # Filtrar películas con datos válidos
        df_filtrado = self.df[
            (self.df['popularity'].notna()) & 
            (self.df['vote_average'].notna()) &
            (self.df['vote_count'] > 10)  # Mínimo 10 votos
        ].copy()
        
        # Crear scatter plot
        fig = px.scatter(
            df_filtrado,
            x='popularity',
            y='vote_average',
            size='vote_count',  # Tamaño del punto = cantidad de votos
            hover_data=['title', 'year'],  # Mostrar al pasar el mouse
            title='Popularidad vs Calificación',
            labels={
                'popularity': 'Popularidad',
                'vote_average': 'Calificación',
                'vote_count': 'Votos'
            },
            color='vote_average',  # Color según calificación
            color_continuous_scale='RdYlGn'  # Rojo-Amarillo-Verde
        )
        
        fig.update_layout(
            xaxis_title='Popularidad',
            yaxis_title='Calificación (0-10)'
        )
        
        return fig
    
    def obtener_top_peliculas(self, n=10, min_votos=100):
        """
        Obtiene las N películas mejor calificadas.
        
        ¿Por qué min_votos?
        - Evita películas con 1 voto de 10/10 que no son representativas
        - Solo considera películas con suficientes votaciones
        
        Parámetros:
        - n: Cuántas películas retornar
        - min_votos: Mínimo de votos requeridos
        
        Returns:
        - DataFrame con las top películas
        """
        # Filtrar por mínimo de votos
        df_filtrado = self.df[self.df['vote_count'] >= min_votos].copy()
        
        # Ordenar por calificación descendente
        top_peliculas = df_filtrado.nlargest(n, 'vote_average')
        
        # Seleccionar columnas relevantes
        return top_peliculas[['title', 'vote_average', 'vote_count', 'year', 'original_language']]


# ============================================
# CLASE PARA LA INTERFAZ: InterfazDashboard
# ============================================
class InterfazDashboard:
    """
    Clase que maneja la interfaz visual con Streamlit.
    
    ¿Por qué separar en otra clase?
    - AnalizadorPeliculas = lógica de datos (backend)
    - InterfazDashboard = presentación visual (frontend)
    - Separación de responsabilidades (buen POO)
    
    Atributos:
    - analizador: Objeto de tipo AnalizadorPeliculas
    """
    
    def __init__(self, analizador):
        """
        Constructor.
        
        Parámetros:
        - analizador: Objeto AnalizadorPeliculas ya creado
        """
        self.analizador = analizador
    
    def configurar_pagina(self):
        """
        Configura la página de Streamlit.
        
        ¿Qué hace?
        - Define título de la pestaña del navegador
        - Define diseño (wide = ancho completo)
        - Configura sidebar
        """
        st.set_page_config(
            page_title="Dashboard de Películas 🎬",
            page_icon="🎬",
            layout="wide"
        )
    
    def mostrar_header(self):
        """
        Muestra el encabezado del dashboard.
        """
        st.title("🎬 Dashboard de Análisis de Películas")
        st.markdown("---")  # Línea divisoria
        st.markdown("""
        **Bienvenido al Dashboard de Películas**
        
        Este dashboard analiza 10,000 películas de la base de datos TMDB.
        Explora las visualizaciones para descubrir tendencias interesantes.
        """)
    
    def mostrar_metricas(self):
        """
        Muestra las métricas principales en la parte superior.
        
        ¿Qué es st.columns?
        - Divide el espacio horizontal en columnas
        - Permite mostrar métricas lado a lado
        """
        # Calcular métricas
        metricas = self.analizador.calcular_metricas()
        
        st.markdown("### 📊 Métricas Generales")
        
        # Crear 5 columnas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Mostrar métrica en cada columna
        with col1:
            st.metric(
                label="Total de Películas",
                value=f"{metricas['total_peliculas']:,}"
            )
        
        with col2:
            st.metric(
                label="Calificación Promedio",
                value=f"{metricas['calificacion_promedio']:.2f}"
            )
        
        with col3:
            st.metric(
                label="Idiomas Únicos",
                value=metricas['total_idiomas']
            )
        
        with col4:
            st.metric(
                label="Año Más Antiguo",
                value=metricas['anio_minimo']
            )
        
        with col5:
            st.metric(
                label="Año Más Reciente",
                value=metricas['anio_maximo']
            )
        
        st.markdown("---")
    
    def mostrar_graficos(self):
        """
        Muestra todos los gráficos del dashboard.
        
        ¿Por qué st.plotly_chart?
        - Renderiza gráficos de Plotly en Streamlit
        - use_container_width=True hace que ocupe todo el ancho
        """
        # GRÁFICO 1: Distribución de Calificaciones
        st.markdown("### 📊 Distribución de Calificaciones")
        st.markdown("*¿Cómo se distribuyen las calificaciones? ¿La mayoría son buenas o malas?*")
        fig1 = self.analizador.grafico_distribucion_calificaciones()
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("---")
        
        # GRÁFICO 2 y 3: Top Idiomas + Evolución Temporal (en 2 columnas)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌍 Top 10 Idiomas")
            st.markdown("*¿Qué industrias cinematográficas dominan el dataset?*")
            fig2 = self.analizador.grafico_top_idiomas()
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Evolución Temporal")
            st.markdown("*¿Cómo ha cambiado la producción a lo largo de los años?*")
            fig3 = self.analizador.grafico_evolucion_temporal()
            st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("---")
        
        # GRÁFICO 4: Popularidad vs Calificación
        st.markdown("### 💎 Popularidad vs Calificación")
        st.markdown("*¿Las películas populares son realmente las mejores? ¿Hay joyas ocultas?*")
        fig4 = self.analizador.grafico_popularidad_vs_calificacion()
        st.plotly_chart(fig4, use_container_width=True)
        
        st.markdown("---")
        
        # GRÁFICO 5: Top Películas (como tabla)
        st.markdown("### 🏆 Top 10 Películas Mejor Calificadas")
        st.markdown("*Películas con mínimo 100 votos*")
        
        top_peliculas = self.analizador.obtener_top_peliculas()
        
        # Mostrar como tabla interactiva
        st.dataframe(
            top_peliculas,
            use_container_width=True,
            hide_index=True
        )
    
    def ejecutar(self):
        """
        Método principal que ejecuta todo el dashboard.
        
        ¿Por qué este método?
        - Orquesta toda la interfaz
        - Llama a todos los métodos en orden
        - Punto de entrada principal
        """
        self.configurar_pagina()
        self.mostrar_header()
        
        # Verificar que los datos se cargaron correctamente
        if self.analizador.df is not None:
            self.mostrar_metricas()
            self.mostrar_graficos()
        else:
            st.error("❌ No se pudieron cargar los datos. Verifica la ruta del archivo.")


# ============================================
# FUNCIÓN MAIN (Punto de entrada)
# ============================================
def main():
    """
    Función principal que inicia la aplicación.
    
    ¿Por qué una función main?
    - Buena práctica de programación
    - Separa la lógica de inicio
    - Facilita testing y reutilización
    """
    # PASO 1: Crear el analizador de películas
    ruta_csv = 'tmdb_movies_clean.csv'  # Cambiar si tu archivo está en otra ubicación
    analizador = AnalizadorPeliculas(ruta_csv)
    
    # PASO 2: Cargar los datos
    if not analizador.cargar_datos():
        st.stop()  # Detener ejecución si falló la carga
    
    # PASO 3: Crear la interfaz
    interfaz = InterfazDashboard(analizador)
    
    # PASO 4: Ejecutar el dashboard
    interfaz.ejecutar()


# ============================================
# EJECUCIÓN DEL PROGRAMA
# ============================================
if __name__ == "__main__":
    """
    ¿Qué es esto?
    - Se ejecuta solo cuando corres este archivo directamente
    - No se ejecuta si importas este archivo en otro
    - Es la "puerta de entrada" del programa
    """
    main()
