import streamlit as st
import google.generativeai as genai
import random
import json
from fpdf import FPDF

# 1. CONFIGURACIÓN DE LA IA (Coloca tu llave aquí)
# Consíguela en: https://aistudio.google.com/app/apikey
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. CONFIGURACIÓN DE PÁGINA "SÍ AL MÉRITO"
st.set_page_config(page_title="SÍ AL MÉRITO - IA Engine", layout="wide")

# Estilo visual pro
st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; height: 3em; font-weight: bold; }
    .stTextInput>div>div>input { border: 2px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# 3. FUNCIÓN PARA GENERAR PREGUNTAS CON IA
def generar_preguntas_ia(tema, nivel, cantidad):
    prompt = f"""
    Actúa como un experto en concursos de la CNSC y leyes colombianas. 
    Genera un examen de {cantidad} preguntas sobre el tema: "{tema}" para nivel {nivel}.
    Las preguntas deben seguir la Taxonomía de Bloom (Juicio Situacional).
    
    IMPORTANTE: Responde ÚNICAMENTE en formato JSON estrictamente como este ejemplo:
    [
      {{
        "p": "¿Pregunta redactada aquí?",
        "o": ["Opción A", "Opción B", "Opción C"],
        "r": "Opción A",
        "s": "Sustento legal detallado aquí"
      }}
    ]
    """
    try:
        response = model.generate_content(prompt)
        # Limpieza simple para asegurar que solo procesamos el JSON
        texto_limpio = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(texto_limpio)
    except Exception as e:
        st.error(f"Error de IA: {e}")
        return None

# 4. FUNCIÓN DE PDF
def crear_pdf_ia(puntaje, resultados, tema):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(200, 10, "SÍ AL MÉRITO - ENTRENAMIENTO IA", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Tema: {tema} | Puntaje: {puntaje}/100", ln=True)
    pdf.ln(5)
    for i, res in enumerate(resultados):
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 7, f"{i+1}. {res['p']}")
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 7, f"Respuesta: {res['u']} (Correcta: {res['c']})", ln=True)
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin-1', errors='ignore')

# 5. LÓGICA DE SESIÓN
if 'fase' not in st.session_state: st.session_state.fase = "config"
if 'es_vip' not in st.session_state: st.session_state.es_vip = False

# 6. PANEL LATERAL
with st.sidebar:
    st.title("🛡️ SÍ AL MÉRITO IA")
    pwd = st.text_input("Código VIP:", type="password")
    if pwd == "CESAR2026": st.session_state.es_vip = True
    
    st.divider()
    nivel_sel = st.selectbox("Nivel de Carrera:", ["Asistencial", "Técnico", "Profesional"])
    cant_sel = st.slider("Cantidad de preguntas:", 3, 20, 5)

# 7. INTERFAZ PRINCIPAL
st.markdown("<h1 style='text-align: center; color: #2e7d32;'>Bunker de Inteligencia Artificial</h1>", unsafe_allow_html=True)

if st.session_state.fase == "config":
    st.info("Escribe el tema que deseas estudiar. La IA construirá el examen basándose en la normativa vigente.")
    tema_input = st.text_input("🎯 ¿Qué tema quieres estudiar hoy?", placeholder="Ej: Ley 1474 de 2011, Gestión Documental, Código de Ética...")
    
    if st.button("🚀 GENERAR EXAMEN AHORA"):
        if tema_input:
            with st.spinner("La IA está redactando tus preguntas..."):
                preguntas = generar_preguntas_ia(tema_input, nivel_sel, cant_sel)
                if preguntas:
                    st.session_state.preguntas = preguntas
                    st.session_state.tema_actual = tema_input
                    st.session_state.respuestas = {}
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("Escribe un tema antes de continuar.")

elif st.session_state.fase == "examen":
    st.subheader(f"Simulacro: {st.session_state.tema_actual}")
    with st.form("quiz_ia"):
        for i, q in enumerate(st.session_state.preguntas):
            st.markdown(f"**{i+1}. {q['p']}**")
            st.session_state.respuestas[i] = st.radio("Opciones:", q['o'], key=f"ia_{i}", index=None)
            st.divider()
        
        if st.form_submit_button("🏁 FINALIZAR"):
            if None in st.session_state.respuestas.values():
                st.error("Por favor responde todas.")
            else:
                st.session_state.fase = "resultados"
                st.rerun()

elif st.session_state.fase == "resultados":
    correctas = sum(1 for i, q in enumerate(st.session_state.preguntas) if st.session_state.respuestas[i] == q['r'])
    puntaje = int((correctas / len(st.session_state.preguntas)) * 100)
    
    st.header(f"Tu Resultado: {puntaje}/100")
    
    for i, q in enumerate(st.session_state.preguntas):
        es_ok = st.session_state.respuestas[i] == q['r']
        with st.expander(f"Pregunta {i+1}: {'✅' if es_ok else '❌'}"):
            st.write(f"**Respuesta:** {q['r']}")
            st.caption(f"Sustento: {q['s']}")

    if st.session_state.es_vip:
        datos_pdf = []
        for i, q in enumerate(st.session_state.preguntas):
            datos_pdf.append({'p': q['p'], 'u': st.session_state.respuestas[i], 'c': q['r'], 's': q['s']})
        
        pdf_bytes = crear_pdf_ia(puntaje, datos_pdf, st.session_state.tema_actual)
        st.download_button("📥 DESCARGAR RESULTADOS PDF", data=pdf_bytes, file_name="Examen_IA.pdf")
    
    if st.button("🔄 HACER OTRO EXAMEN"):
        st.session_state.fase = "config"
        st.rerun()
