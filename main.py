import streamlit as st
import random
from fpdf import FPDF
import base64

# CONFIGURACIÓN DE MARCA SÍ AL MÉRITO
st.set_page_config(page_title="SÍ AL MÉRITO - Generador Universal", layout="wide")

# --- FUNCIONES DE SOPORTE ---
def crear_pdf(nombre, puntaje, resultados, nivel, tema):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(200, 10, "REPORTE DE RESULTADOS - SÍ AL MÉRITO", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, f"Aspirante: {nombre} | Nivel: {nivel}", ln=True, align='C')
    pdf.cell(200, 10, f"Eje Temático: {tema}", ln=True, align='C')
    pdf.cell(200, 10, f"Puntaje Final: {puntaje}/100", ln=True, align='C')
    pdf.ln(10)
    
    for res in resultados:
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 8, f"Pregunta: {res['p']}")
        pdf.set_font("Arial", size=10)
        color = (46, 125, 50) if res['u'] == res['c'] else (200, 0, 0)
        pdf.set_text_color(*color)
        pdf.multi_cell(0, 8, f"Tu respuesta: {res['u']} | Correcta: {res['c']}")
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 8, f"Sustento Legal: {res['s']}")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)
    return pdf.output(dest='S').encode('latin-1')

# --- BANCO DE PREGUNTAS UNIVERSAL ---
# César: Aquí es donde vas a "alimentar" al sistema. 
# Solo copia el bloque y cambia el nombre del tema.
preguntas_db = {
    "Ley 1755 (Derecho de Petición)": [
        {"p": "¿Plazo para peticiones de documentos?", "o": ["10 días", "15 días", "30 días"], "r": "10 días", "s": "Art. 14 Ley 1755."},
        # Agrega más aquí...
    ],
    "Código General Disciplinario": [
        {"p": "¿Cuál es la falta gravísima?", "o": ["Dolo", "Culpa leve", "Error"], "r": "Dolo", "s": "Ley 1952 de 2019."},
    ],
    "Contratación Estatal (Ley 80)": [
        {"p": "¿Cuál es un principio de la contratación?", "o": ["Transparencia", "Secreto", "Lucro"], "r": "Transparencia", "s": "Ley 80 de 1993."},
    ],
    "Gestión Documental": [
        {"p": "¿Qué es un fondo acumulado?", "o": ["Documentos sin criterio", "Archivo histórico", "Bodega"], "r": "Documentos sin criterio", "s": "Ley 594 de 2000."}
    ]
}

# GESTIÓN DE SESIÓN
if 'examen_finalizado' not in st.session_state: st.session_state.examen_finalizado = False
if 'es_vip' not in st.session_state: st.session_state.es_vip = False

# PANEL LATERAL
with st.sidebar:
    st.title("🛡️ Panel de Control")
    clave = st.text_input("Código de Acceso:", type="password")
    if clave == "CESAR2026":
        st.session_state.es_vip = True
        st.success("💎 MODO VIP ACTIVADO")
    
    nivel = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional", "Asesor"])
    tema = st.selectbox("Eje Temático:", list(preguntas_db.keys()))
    
    opciones_cant = [20, 50, 100] if st.session_state.es_vip else [5, 10, 15]
    cantidad = st.select_slider("Cantidad de preguntas:", options=opciones_cant)

    if st.button("🚀 INICIAR SIMULACRO"):
        st.session_state.preguntas = random.sample(preguntas_db[tema], min(len(preguntas_db[tema]), cantidad))
        st.session_state.examen_finalizado = False
        st.session_state.respuestas = {}
        st.session_state.tema_actual = tema

# INTERFAZ DE EXAMEN
if 'preguntas' in st.session_state:
    st.markdown(f"### 📋 {st.session_state.tema_actual} - Nivel {nivel}")
    with st.form("examen"):
        for i, q in enumerate(st.session_state.preguntas):
            st.markdown(f"**{i+1}. {q['p']}**")
            st.session_state.respuestas[i] = st.radio("Seleccione respuesta:", q['o'], key=f"pre_{i}")
            st.write("---")
        
        if st.form_submit_button("🏁 FINALIZAR Y CALIFICAR"):
            correctas = sum(1 for i, q in enumerate(st.session_state.preguntas) if st.session_state.respuestas[i] == q['r'])
            puntaje = (correctas / len(st.session_state.preguntas)) * 100
            
            st.metric("TU PUNTAJE", f"{int(puntaje)} / 100")
            
            if st.session_state.es_vip:
                st.balloons()
                res_lista = []
                for i, q in enumerate(st.session_state.preguntas):
                    res_lista.append({'p': q['p'], 'u': st.session_state.respuestas[i], 'c': q['r'], 's': q['s']})
                
                pdf_bytes = crear_pdf("Aspirante Meritorio", int(puntaje), res_lista, nivel, st.session_state.tema_actual)
                st.download_button("📥 DESCARGAR REPORTE PDF", data=pdf_bytes, file_name=f"Resultado_{st.session_state.tema_actual}.pdf", mime="application/pdf")
            else:
                st.info("Para descargar el PDF con el sustento legal de cada respuesta, activa tu Código VIP.")
