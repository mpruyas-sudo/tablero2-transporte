import streamlit as st
import pandas as pd

# Configuracion de la pagina
st.set_page_config(page_title="Tablero de Transporte", layout="wide", page_icon="??")

# Titulo principal
st.title("Control de Viajes por Medio de Transporte")
st.markdown("Analisis de la cantidad de viajes diarios segun el tipo de transporte publico.(archivo excel-prueba)")

# 1. Cargar y preparar los datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("transporte.csv", encoding='latin-1')
    # Convertir la columna de tiempo a formato fecha para facilitar los filtros
    df['indice_tiempo'] = pd.to_datetime(df['indice_tiempo'])
    return df

try:
    df = cargar_datos()

    # 2. Barra lateral con filtros
    st.sidebar.header("Filtros de Tiempo")
    
    # Selector de rango de fechas basado en los datos reales del CSV
    fecha_min = df['indice_tiempo'].min().date()
    fecha_max = df['indice_tiempo'].max().date()
    
    fechas_seleccionadas = st.sidebar.date_input(
        "Seleccionar rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max
    )

    # Filtrar el DataFrame segun las fechas elegidas
    # Verificacion de que el usuario haya seleccionado ambas fechas (inicio y fin)
    if isinstance(fechas_seleccionadas, tuple) and len(fechas_seleccionadas) == 2:
        inicio, fin = fechas_seleccionadas
        df_filtrado = df[(df['indice_tiempo'].dt.date >= inicio) & (df['indice_tiempo'].dt.date <= fin)]
    else:
        df_filtrado = df

    # 3. Seccion de Metricas Principales (KPIs)
    st.subheader("Resumen del Periodo Seleccionado")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Total General", f"{df_filtrado['total'].sum():,}")
    col2.metric("Colectivo", f"{df_filtrado['colectivo'].sum():,}")
    col3.metric("Subte", f"{df_filtrado['subte'].sum():,}")
    col4.metric("Tren", f"{df_filtrado['tren'].sum():,}")
    col5.metric("Lancha", f"{df_filtrado['lancha'].sum():,}")

    st.markdown("---")

    # 4. Grafico de Evolucion Temporal
    st.subheader("?? Evolucion Temporal por Medio de Transporte")
    
    # Preparar los datos para el grafico de lineas (indexado por fecha y sin la columna 'total')
    df_grafico = df_filtrado.set_index('indice_tiempo')[['colectivo', 'subte', 'tren', 'lancha']]
    
    # Selector interactivo para que el usuario elija que transportes ver en el grafico
    medios_disponibles = ['colectivo', 'subte', 'tren', 'lancha']
    medios_seleccionados = st.multiselect(
        "Seleccionar medios de transporte para comparar:",
        options=medios_disponibles,
        default=medios_disponibles
    )
    
    if medios_seleccionados:
        st.line_chart(df_grafico[medios_seleccionados])
    else:
        st.warning("Por favor, selecciona al menos un medio de transporte para visualizar el grafico.")

    st.markdown("---")

    # 5. Visualizacion de los datos en bruto
    if st.checkbox("Mostrar tabla de datos detallada"):
        st.subheader("?? Datos en Bruto")
        # Formatear la fecha para que se vea mas limpia en la tabla
        df_tabla = df_filtrado.copy()
        df_tabla['indice_tiempo'] = df_tabla['indice_tiempo'].dt.strftime('%Y-%m-%d')
        st.dataframe(df_tabla, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Ocurrio un error al procesar la aplicacion: {e}")
    st.info("Por favor, verifica que el archivo 'transporte.csv' este ubicado en la misma carpeta que este script.")
