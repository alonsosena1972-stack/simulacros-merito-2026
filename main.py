import streamlit as st
import google.generativeai as genai
import json
import re

# ================= 1. CONFIGURACIÓN DE ACCESO =================
# IMPORTANTE: Si esto falla, por favor genera una NUEVA llave en Google AI Studio.
# La llave actual puede estar restringida por tantos intentos fallidos.
API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=API_KEY)

@st.cache_resource
def iniciar_cerebro_ia():
    # Intentamos cargar el modelo con nombres alternativos para evitar el 404
    for nombre_modelo in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']:
        try:
            m = genai.GenerativeModel(nombre_modelo)
            # Prueba de vida rápida
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = iniciar_cerebro_ia()

# ================= 2. INTERFAZ VISUAL PROFESIONAL =================
st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .stButton>button { 
        background: linear-gradient(90deg, #1b5e20 0%, #2e7d32 100%); 
        color: white; border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%;
    }
    .stTextInput>div>div>input { border: 2px solid #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# ================= 3. FUNCIÓN DE GENERACIÓN (BLINDADA) =================
def generar_preguntas(tema, nivel):
    # Usamos formato de texto limpio para evitar el ValueError de Python
    instruccion = (
        "Actúa como experto de la CNSC Colombia. Genera 3 preguntas de opción múltiple "
        "sobre el tema: " + tema + " para nivel " + nivel + ". "
        "Responde ÚNICAMENTE un JSON con este formato: "
        '[{"p":"pregunta","o":["A","B","C"],"r":"A","s":"sustento"}]'
    )
    
    try:
        response = model.generate_content(instruccion)
        texto_sucio = response.text.strip()
        
        # Extraemos solo el contenido entre los corchetes [ ]
        match = re.search(r"\[.*\]", texto_sucio, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(texto_sucio)
    except Exception as e:
        st.error("La IA no pudo procesar la solicitud. Detalles: " + str(e))
        return None

# ================= 4. FLUJO DE USUARIO =================
st.title("🏆 SÍ AL MÉRITO - Búnker IA")
st.write("---")

if model is None:
    st.error("⚠️ No se pudo establecer conexión con los servidores de Google. Esto suele ser un problema de la API Key. Por favor, genera una nueva en Google AI Studio.")
    st.stop()

if 'examen' not in st.session_state:
    st.subheader("Configura tu simulacro")
    tema_input = st.text_input("🎯 Tema (Ej: Ley 1437 de 2011):")
    nivel_input = st.selectbox("Nivel del cargo:", ["Asistencial", "Técnico", "Profesional"])
    
    if st.button("🚀 GENERAR EXAMEN"):
        if tema_input:
            with st.spinner("🤖 La IA está redactando tus preguntas..."):
                resultado = generar_preguntas(tema_input, nivel_input)
                if resultado:
                    st.session_state.examen = resultado
                    st.rerun()
        else:
            st.warning("Escribe un tema para estudiar.")
else:
    st.subheader("📝 Simulacro Generado")
    for i, q in enumerate(st.session_state.examen):
        st.markdown("**" + str(i+1) + ". " + q['p'] + "**")
        st.radio("Opciones:", q['o'], key="pregunta_" + str(i), index=None)
        with st.expander("Ver Sustento Legal"):
            st.info(q['s'])
        st.write("---")
    
    if st.button("🔄 Crear otro simulacro"):
        del st.session_state.examen
        st.rerun()
