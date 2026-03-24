# ============================================
# DASHBOARD DE PELÍCULAS - STREAMLIT
# ============================================

# IMPORTACIONES
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# CLASE PRINCIPAL: AnalizadorPeliculas
# ============================================
class AnalizadorPeliculas:
    
    def __init__(self, ruta_archivo):

        # Ruta de la laptop de Mau
        #self.ruta_archivo = r"C:\Movie_Insigths\data\processed\tmdb_movies_clean.csv"

        # Ruta de la laptop de Josué
        self.ruta_archivo = r"C:\Users\harir\OneDrive\Documents\AAA_Progra2\Proyecto_2\data\processed\tmdb_movies_clean.csv"
        self.df = None  # Inicialmente vacío
    
    def cargar_datos(self):

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

        metricas = {
            'total_peliculas': len(self.df),
            'calificacion_promedio': self.df['vote_average'].mean(),
            'total_idiomas': self.df['original_language'].nunique(),
            'anio_minimo': int(self.df['year'].min()) if self.df['year'].notna().any() else 0,
            'anio_maximo': int(self.df['year'].max()) if self.df['year'].notna().any() else 0
        }
        return metricas
    
    def grafico_distribucion_calificaciones(self):

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

        # Filtrar años válidos (no NaN)
        df_con_anio = self.df[self.df['year'].notna()].copy()
        
        # Contar películas por año
        peliculas_por_anio = df_con_anio.groupby('year').size().reset_index(name='cantidad')
        
        # Crear gráfico de línea
        fig = px.line(
            peliculas_por_anio,
            x='year',
            y='cantidad',
            title='Evolución de la Producción Cinematográfica entre el año 2020 y el año 2025',
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

        # Filtrado de votos
        df_filtrado = self.df[self.df['vote_count'] >= min_votos].copy()
        
        # Ordenamiento descendente
        top_peliculas = df_filtrado.nlargest(n, 'vote_average')
        
        # Columnas relevantes
        return top_peliculas[['title', 'vote_average', 'vote_count', 'year', 'original_language']]


# ============================================
# CLASE PARA LA INTERFAZ: InterfazDashboard
# ============================================
class InterfazDashboard:
    
    def __init__(self, analizador):

        self.analizador = analizador
    
    def configurar_pagina(self):

        st.set_page_config(
            page_title="Dashboard de Películas 🎬",
            page_icon="🎬",
            layout="wide"
        )
    
    def mostrar_header(self):

        st.title("🎬 Dashboard de Análisis de Películas")
        st.markdown("---")  # Línea divisoria
        st.markdown("""
        **Bienvenido al Dashboard de Películas de The Movie Database**
        
        Este dashboard analiza 10,000 películas de la base de datos TMDB.
        """)
    
    def mostrar_metricas(self):

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

        # GRÁFICO 1: Distribución de Calificaciones
        st.markdown("### 📊 Distribución de Calificaciones")
        st.markdown("*¿Cómo se distribuyen las calificaciones?*")
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
        st.markdown("*¿Las películas populares son realmente las mejores?*")
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

        self.configurar_pagina()
        self.mostrar_header()
        
        # Verificar que los datos se cargaron correctamente
        if self.analizador.df is not None:
            self.mostrar_metricas()
            self.mostrar_graficos()
        else:
            st.error("No se pudieron cargar los datos. Verifica la ruta del archivo.")



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
    ruta_csv = 'tmdb_movies_clean.csv'
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
    main()
