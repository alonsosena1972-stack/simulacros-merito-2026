import streamlit as st
import random
from fpdf import FPDF

# CONFIGURACIÓN DE MARCA
st.set_page_config(page_title="SÍ AL MÉRITO - Sistema Pro", layout="wide")

# --- LÓGICA DE PDF ---
def crear_pdf(nombre, puntaje, resultados, nivel, tema):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "SÍ AL MÉRITO - REPORTE PROFESIONAL", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Eje Temático: {tema} | Puntaje: {puntaje}/100", ln=True)
    pdf.ln(5)
    for res in resultados:
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 10, f"P: {res['p']}")
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Respuesta: {res['u']} | Correcta: {res['c']}", ln=True)
        pdf.set_text_color(100)
        pdf.multi_cell(0, 10, f"Sustento: {res['s']}")
        pdf.set_text_color(0)
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1')

# --- BASE DE DATOS (Agrega lo que quieras aquí) ---
preguntas_db = {
    "Gestión Documental": [
        {"p": "¿Qué es un fondo acumulado?", "o": ["Documentos sin criterio", "Archivo histórico", "Bodega"], "r": "Documentos sin criterio", "s": "Según el AGN, son documentos reunidos sin criterios archivísticos."},
    ],
    "Ley 1755 (Peticiones)": [
        {"p": "¿Plazo para responder documentos?", "o": ["10 días", "15 días", "30 días"], "r": "10 días", "s": "Art. 14 Ley 1755."},
    ]
}

# ESTADO DE SESIÓN
if 'examen_terminado' not in st.session_state: st.session_state.examen_terminado = False
if 'es_vip' not in st.session_state: st.session_state.es_vip = False

# PANEL IZQUIERDO
with st.sidebar:
    st.header("🏆 SÍ AL MÉRITO")
    clave = st.text_input("Código VIP:", type="password")
    if clave == "CESAR2026": st.session_state.es_vip = True
    
    tema = st.selectbox("Eje Temático:", list(preguntas_db.keys()))
    cantidad = st.slider("Preguntas:", 1, 100, 5)
    
    if st.button("🚀 EMPEZAR"):
        st.session_state.preguntas = random.sample(preguntas_db[tema], min(len(preguntas_db[tema]), cantidad))
        st.session_state.examen_terminado = False
        st.session_state.respuestas_usuario = {}

# CUERPO PRINCIPAL (DERECHA)
st.markdown("<h1 style='color: #2e7d32;'>SÍ AL MÉRITO: Centro de Entrenamiento</h1>", unsafe_allow_html=True)

if 'preguntas' in st.session_state and not st.session_state.examen_terminado:
    with st.form("cuestionario"):
        for i, q in enumerate(st.session_state.preguntas):
            st.markdown(f"**{i+1}. {q['p']}**")
            st.session_state.respuestas_usuario[i] = st.radio("Opciones:", q['o'], key=f"q_{i}")
        
        if st.form_submit_button("FINALIZAR"):
            st.session_state.examen_terminado = True
            st.rerun() # Esto refresca la página para salir del form

# MOSTRAR RESULTADOS (FUERA DEL FORMULARIO)
if st.session_state.examen_terminado:
    correctas = sum(1 for i, q in enumerate(st.session_state.preguntas) if st.session_state.respuestas_usuario[i] == q['r'])
    puntaje = int((correctas / len(st.session_state.preguntas)) * 100)
    
    st.success(f"### Tu Puntaje: {puntaje} / 100")
    
    if st.session_state.es_vip:
        st.balloons()
        res_lista = []
        for i, q in enumerate(st.session_state.preguntas):
            res_lista.append({'p': q['p'], 'u': st.session_state.respuestas_usuario[i], 'c': q['r'], 's': q['s']})
        
        pdf_bytes = crear_pdf("Aspirante", puntaje, res_lista, "Técnico", tema)
        st.download_button("📥 DESCARGAR RESULTADOS PDF", data=pdf_bytes, file_name="Resultado_SiAlMerito.pdf", mime="application/pdf")
    else:
        st.warning("Puntaje registrado. El PDF es para miembros VIP.")
