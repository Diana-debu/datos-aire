import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import numpy as np
from streamlit_option_menu import option_menu

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Calidad del Aire",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('ambiente_calidad_aire.csv')
    return df

df = load_data()

# Paleta de colores profesional
COLORS = {
    'primary': '#2E8B57',  # Verde bosque
    'secondary': '#4682B4',  # Azul acero
    'accent': '#FF6B6B',    # Coral suave
    'background': '#F8F9FA',
    'text': '#2C3E50'
}

# Estilos CSS personalizados
st.markdown(f"""
<style>
    .main {{
        background-color: {COLORS['background']};
    }}
    .css-1d391kg {{
        padding: 2rem 1rem;
    }}
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid {COLORS['primary']};
    }}
    .section-header {{
        color: {COLORS['primary']};
        border-bottom: 2px solid {COLORS['primary']};
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# Navegación en sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2978/2978373.png", width=80)
    st.title("🌿 Calidad del Aire")
    
    selected = option_menu(
        menu_title="Navegación",
        options=["Inicio", "Análisis Descriptivo", "Mapa Interactivo"],
        icons=["house", "bar-chart", "map"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": COLORS['primary'], "font-size": "16px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#e9ecef"},
            "nav-link-selected": {"background-color": COLORS['primary']},
        }
    )

# Página 1: Inicio y Contexto
if selected == "Inicio":
    st.markdown(f"<h1 style='color: {COLORS['primary']};'>Sistema de Análisis de Calidad del Aire</h1>", unsafe_allow_html=True)
    st.markdown("### Plataforma de monitoreo y análisis de indicadores ambientales")
    
    st.markdown("""
    Esta aplicación permite analizar y visualizar datos de calidad del aire recolectados 
    en diferentes departamentos de Colombia. Explore las diferentes secciones para:
    
    - 📊 **Análisis descriptivo** de los indicadores ambientales
    - 🗺️ **Visualización geográfica** de la calidad del aire
    - 📈 **Tendencias y patrones** por categorías y departamentos
    """)
    
    # Métricas principales
    st.markdown("---")
    st.markdown("<h3 class='section-header'>Resumen Ejecutivo</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h4 style='color: {COLORS['text']}; margin: 0;'>📈 Total de Registros</h4>
            <h2 style='color: {COLORS['primary']}; margin: 0;'>{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h4 style='color: {COLORS['text']}; margin: 0;'>🏙️ Departamentos</h4>
            <h2 style='color: {COLORS['primary']}; margin: 0;'>{df['Departamento'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_value = df['Valor'].mean()
        st.markdown(f"""
        <div class='metric-card'>
            <h4 style='color: {COLORS['text']}; margin: 0;'>📊 Valor Promedio</h4>
            <h2 style='color: {COLORS['primary']}; margin: 0;'>{avg_value:.3f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h4 style='color: {COLORS['text']}; margin: 0;'>📋 Categorías</h4>
            <h2 style='color: {COLORS['primary']}; margin: 0;'>{df['Categoría'].nunique()}</h2>
        </div>
        """, unsafe_allow_html=True)

# Página 2: Análisis Descriptivo
elif selected == "Análisis Descriptivo":
    st.markdown(f"<h1 style='color: {COLORS['primary']};'>📊 Análisis Descriptivo</h1>", unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        departamentos = ['Todos'] + sorted(df['Departamento'].unique().tolist())
        departamento_seleccionado = st.selectbox(
            "Seleccionar Departamento:",
            departamentos
        )
    
    with col2:
        categorias = ['Todas'] + sorted(df['Categoría'].unique().tolist())
        categoria_seleccionada = st.selectbox(
            "Seleccionar Categoría:",
            categorias
        )
    
    with col3:
        rango_valor = st.slider(
            "Rango de Valor:",
            min_value=float(df['Valor'].min()),
            max_value=float(df['Valor'].max()),
            value=(float(df['Valor'].min()), float(df['Valor'].max())),
            step=0.01
        )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if departamento_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Departamento'] == departamento_seleccionado]
    if categoria_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria_seleccionada]
    df_filtrado = df_filtrado[
        (df_filtrado['Valor'] >= rango_valor[0]) & 
        (df_filtrado['Valor'] <= rango_valor[1])
    ]
    
    # Mostrar datos filtrados
    st.markdown(f"<h3 class='section-header'>Datos Filtrados ({len(df_filtrado)} registros)</h3>", unsafe_allow_html=True)
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Visualizaciones
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h4>Distribución por Categoría</h4>", unsafe_allow_html=True)
        
        # Gráfico de barras con Plotly
        cat_counts = df_filtrado['Categoría'].value_counts()
        fig_bar = px.bar(
            x=cat_counts.index,
            y=cat_counts.values,
            labels={'x': 'Categoría', 'y': 'Cantidad'},
            color=cat_counts.index,
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']]
        )
        fig_bar.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("<h4>Distribución de Valores</h4>", unsafe_allow_html=True)
        
        # Histograma con Plotly
        fig_hist = px.histogram(
            df_filtrado,
            x='Valor',
            nbins=20,
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_hist.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_title='Valor',
            yaxis_title='Frecuencia'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Gráfico adicional: Boxplot por categoría
    st.markdown("<h4>Distribución de Valores por Categoría</h4>", unsafe_allow_html=True)
    fig_box = px.box(
        df_filtrado,
        x='Categoría',
        y='Valor',
        color='Categoría',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    )
    fig_box.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Página 3: Mapa Interactivo
elif selected == "Mapa Interactivo":
    st.markdown(f"<h1 style='color: {COLORS['primary']};'>🗺️ Mapa Interactivo de Calidad del Aire</h1>", unsafe_allow_html=True)
    
    # Filtros para el mapa
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("<h4>Configuración del Mapa</h4>", unsafe_allow_html=True)
        
        categoria_mapa = st.selectbox(
            "Categoría para el mapa:",
            ['Todas'] + sorted(df['Categoría'].unique().tolist()),
            key='mapa_cat'
        )
        
        tamaño_punto = st.slider(
            "Tamaño de los puntos:",
            min_value=1,
            max_value=20,
            value=8
        )
        
        opacidad = st.slider(
            "Opacidad de los puntos:",
            min_value=0.1,
            max_value=1.0,
            value=0.7
        )
    
    # Preparar datos para el mapa
    df_mapa = df.copy()
    if categoria_mapa != 'Todas':
        df_mapa = df_mapa[df_mapa['Categoría'] == categoria_mapa]
    
    # Crear mapa base centrado en Colombia
    m = folium.Map(
        location=[4.5709, -74.2973],  # Centro de Colombia
        zoom_start=6,
        tiles='CartoDB positron'
    )
    
    # Añadir puntos al mapa
    for idx, row in df_mapa.iterrows():
        # Color basado en la categoría
        color_categoria = {
            'A': COLORS['primary'],
            'B': COLORS['secondary'], 
            'C': COLORS['accent']
        }.get(row['Categoría'], '#666666')
        
        # Tamaño basado en el valor (normalizado)
        tamaño_normalizado = tamaño_punto * (row['Valor'] / df_mapa['Valor'].max())
        
        # Crear popup informativo
        popup_text = f"""
        <b>Departamento:</b> {row['Departamento']}<br>
        <b>Categoría:</b> {row['Categoría']}<br>
        <b>Valor:</b> {row['Valor']:.4f}<br>
        <b>Coordenadas:</b> {row['Latitud']:.4f}, {row['Longitud']:.4f}
        """
        
        # Añadir marcador
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=tamaño_normalizado,
            popup=folium.Popup(popup_text, max_width=300),
            color=color_categoria,
            fill=True,
            fillColor=color_categoria,
            fillOpacity=opacidad,
            weight=1
        ).add_to(m)
    
    # Mostrar el mapa
    with col2:
        folium_static(m, width=800, height=600)
    
    # Estadísticas del mapa
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Puntos en el mapa", len(df_mapa))
    
    with col2:
        st.metric("Valor promedio", f"{df_mapa['Valor'].mean():.4f}")
    
    with col3:
        st.metric("Departamentos representados", df_mapa['Departamento'].nunique())
    
    # Tabla de datos del mapa
    st.markdown("<h4>Datos del Mapa</h4>", unsafe_allow_html=True)
    st.dataframe(df_mapa[['Departamento', 'Categoría', 'Valor', 'Latitud', 'Longitud']], use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Sistema de Análisis de Calidad del Aire • Desarrollado con Streamlit"
    "</div>", 
    unsafe_allow_html=True
)