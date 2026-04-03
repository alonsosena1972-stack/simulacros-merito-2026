import streamlit as st
import random
from fpdf import FPDF
import base64

# CONFIGURACIÓN DE MARCA SÍ AL MÉRITO
st.set_page_config(page_title="SÍ AL MÉRITO - VIP", layout="wide")

# LÓGICA DE PDF PARA VIPs
def crear_pdf(nombre, puntaje, resultados, nivel):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "REPORTE DE RESULTADOS - SÍ AL MÉRITO", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Aspirante: {nombre} | Nivel: {nivel}", ln=True, align='C')
    pdf.cell(200, 10, f"Puntaje Final: {puntaje}/100", ln=True, align='C')
    pdf.ln(10)
    
    for res in resultados:
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 10, f"Pregunta: {res['p']}")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, f"Tu respuesta: {res['u']} | Correcta: {res['c']}")
        pdf.set_text_color(46, 125, 50)
        pdf.multi_cell(0, 10, f"Sustento Legal: {res['s']}")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

# --- BASE DE DATOS (EJEMPLO - AQUÍ VAN TUS EJES) ---
preguntas_db = {
    "Ley 1755 (Peticiones)": [
        {"p": "¿Plazo para peticiones de documentos?", "o": ["10 días", "15 días", "30 días"], "r": "10 días", "s": "Art. 14 Ley 1755: Las peticiones de documentos deben resolverse en 10 días."},
        # Agregar aquí las 100 preguntas por tema...
    ]
}

# GESTIÓN DE SESIÓN
if 'examen_finalizado' not in st.session_state: st.session_state.examen_finalizado = False
if 'es_vip' not in st.session_state: st.session_state.es_vip = False

# PANEL DE ACCESO
with st.sidebar:
    st.image("https://tu-logo-url.com", width=200) # Opcional: Tu logo
    codigo = st.text_input("🔑 Código VIP (Opcional):", type="password")
    if codigo == "CESAR2026": # Tu clave maestra actual
        st.session_state.es_vip = True
        st.success("MODO VIP ACTIVADO")
    
    nivel = st.selectbox("Nivel de Carrera:", ["Asistencial", "Técnico", "Profesional", "Asesor"])
    tema = st.selectbox("Eje Temático:", list(preguntas_db.keys()))
    
    max_preguntas = 100 if st.session_state.es_vip else 15
    cantidad = st.select_slider("Cantidad de Preguntas:", options=[10, 20, 50, 100] if st.session_state.es_vip else [5, 10, 15])

    if st.button("🚀 INICIAR"):
        st.session_state.preguntas = random.sample(preguntas_db[tema], min(len(preguntas_db[tema]), cantidad))
        st.session_state.examen_finalizado = False
        st.session_state.respuestas = {}

# INTERFAZ DE EXAMEN
if 'preguntas' in st.session_state:
    with st.form("simulacro"):
        for i, q in enumerate(st.session_state.preguntas):
            st.markdown(f"**{i+1}. {q['p']}**")
            st.session_state.respuestas[i] = st.radio("Opciones:", q['o'], key=f"r_{i}")
        
        enviar = st.form_submit_button("CALIFICAR")
        
        if enviar:
            correctas = sum(1 for i, q in enumerate(st.session_state.preguntas) if st.session_state.respuestas[i] == q['r'])
            puntaje = (correctas / len(st.session_state.preguntas)) * 100
            
            st.metric("Puntaje Final", f"{puntaje}/100")
            
            if st.session_state.es_vip:
                st.balloons()
                # Preparar datos para el PDF
                lista_resultados = []
                for i, q in enumerate(st.session_state.preguntas):
                    lista_resultados.append({'p': q['p'], 'u': st.session_state.respuestas[i], 'c': q['r'], 's': q['s']})
                
                pdf_data = crear_pdf("Aspirante VIP", puntaje, lista_resultados, nivel)
                st.download_button("📥 DESCARGAR REPORTE PDF", data=pdf_data, file_name="resultado_vip.pdf", mime="application/pdf")
            else:
                st.info("Puntaje registrado. Los reportes PDF son exclusivos para miembros VIP.")
