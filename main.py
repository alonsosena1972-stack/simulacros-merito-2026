import streamlit as st
import google.generativeai as genai
import json
import re

# ================= 1. CONFIGURACIÓN TÉCNICA =================
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# Lógica de Autodeteción: Prueba modelos del más nuevo al más viejo
@st.cache_resource
def cargar_modelo_seguro():
    modelos_a_probar = [
        'gemini-1.5-flash', 
        'models/gemini-1.5-flash', 
        'gemini-pro', 
        'models/gemini-pro'
    ]
    for nombre in modelos_a_probar:
        try:
            m = genai.GenerativeModel(nombre)
            # Prueba rápida de conexión
            m.generate_content("hola", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = cargar_modelo_seguro()

# ================= 2. INTERFAZ SÍ AL MÉRITO =================
st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide")

if not model:
    st.error("❌ ERROR DE SISTEMA: Google no reconoce tu API Key o los modelos están desactivados en tu región.")
    st.stop()

# ================= 3. MOTOR DE GENERACIÓN =================
def generar_simulacro_ia(tema, nivel, cantidad):
    prompt = (
        f"Genera un examen de {cantidad} preguntas sobre '{tema}' para nivel {nivel} en Colombia. "
        f"Responde ÚNICAMENTE un array JSON puro: "
        f"[{{'p': 'pregunta', 'o': ['A', 'B', 'C', 'D'], 'r': 'Opción Correcta', 's': 'Sustento'}}] "
    )
    try:
        response = model.generate_content(prompt)
        res_text = response.text.strip()
        
        # Limpiador de seguridad para extraer el JSON
        match = re.search(r"\[.*\]", res_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(res_text)
    except Exception as e:
        st.error(f"⚠️ Error de respuesta IA: {e}")
        return None

# ================= 4. NAVEGACIÓN DEL BÚNKER =================
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.title("🏆 SÍ AL MÉRITO: Búnker de IA")

if st.session_state.fase == "inicio":
    tema = st.text_input("🎯 Tema (Ej: Ley 1437):")
    nivel = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
    cant = st.slider("Preguntas:", 3, 10, 5)
    
    if st.button("🚀 CONSTRUIR EXAMEN"):
        if tema:
            with st.spinner("Conectando con la red neuronal..."):
                data = generar_simulacro_ia(tema, nivel, cant)
                if data:
                    st.session_state.preguntas = data
                    st.session_state.fase = "examen"
                    st.rerun()

elif st.session_state.fase == "examen":
    for i, item in enumerate(st.session_state.preguntas):
        st.write(f"**{i+1}. {item['p']}**")
        st.radio("Opciones:", item['o'], key=f"p_{i}")
        st.divider()
    
    if st.button("🔄 Volver"):
        st.session_state.fase = "inicio"
        st.rerun()
