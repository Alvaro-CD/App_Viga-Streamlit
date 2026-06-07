import matplotlib.pyplot as plt
import streamlit as st
from anastruct import SystemElements

# Configuración de la página
st.set_page_config(page_title="Viga Biapoyada - AnaStruct", layout="wide")
st.title("📊 Análisis de Viga Biapoyada con Carga Puntual")
st.write(
    "Introduce los parámetros en la barra lateral para calcular los esfuerzos."
)

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("Parámetros de la Viga")

# Longitud de la viga
L = st.sidebar.number_input(
    "Longitud de la viga (m)", min_value=1.0, max_value=10.0, value=6.0, step=0.5
)

# Posición de la carga
x_p = st.sidebar.slider(
    "Posición de la carga (m)", min_value=0.0, max_value=float(L), value=L / 2, step=0.1
)

# Magnitud de la carga (en kN)
P = st.sidebar.number_input(
    "Magnitud de la carga (kN) hacia abajo", min_value=-100.0, max_value=-10.0, value=-50.0, step=5.0
)

# --- CÁLCULO CON ANASTRUCT ---
# Inicializar el sistema estructural
ss = SystemElements()

# Añadir los elementos
ss.add_element(location=[[0, 0], [x_p, 0]])
ss.add_element(location=[[x_p, 0], [L, 0]])

# Añadir apoyos (viga biapoyada: articulado a la izquierda, rodillo a la derecha)
ss.add_support_hinged(node_id=1)
ss.add_support_roll(node_id=3, direction='x') 

# Añadir la carga puntual
ss.point_load(node_id=2, Fy=P)

# Resolver el sistema
ss.solve()

# --- INTERFAZ DE RESULTADOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📐 Estructura y Carga")
    # fig1, ax = plt.subplots()
    # fig1 = ss.show_structure()
    ss.show_structure()
    fig = plt.gcf() # gcf = get current figure. Necesario para almacenar la figura de anastruct y no fallar.
    st.pyplot(fig)
    # plt.clf()

with col2:
    st.subheader("📉 Momento Flector (M)")
    ss.show_bending_moment()
    fig = plt.gcf()
    st.pyplot(fig)

with col1:
    st.subheader("📊 Esfuerzo Cortante (V)")
    ss.show_shear_force()
    fig = plt.gcf()
    st.pyplot(fig)

# --- REACCIONES EN LOS APOYOS ---
st.divider()
st.subheader("🔄 Reacciones en los Apoyos")
reacciones = ss.get_node_results_system(node_id=1)['Fy'], ss.get_node_results_system(node_id=-1)['Fy'] # (node_id=-1) = Último nodo de la lista.

# Formatear la salida de las reacciones
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.metric(label="Reacción vertical (Apoyo Izquierdo)", value=f"{abs(reacciones[0]):.2f} kN")
with col_r2:
    st.metric(label="Reacción vertical (Apoyo Derecho)", value=f"{abs(reacciones[1]):.2f} kN")