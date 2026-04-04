import streamlit as st
import google.generativeai as genai
import json

# 1. Configuración de Acceso con Protocolo de Reintento
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# 2. SELECCIÓN DE MODELO CON RUTA DE RECURSO (Solución al Error 404)
# Esta es la ruta completa que exige la API v1beta
MODEL_NAME = 'models/gemini-1.5-flash-latest'
model = genai.GenerativeModel(model_name=MODEL_NAME)

st.set_page_config(page_title="SÍ AL MÉRITO - Sistema IA", layout="wide")

# Estilo Profesional de la Plataforma
st.markdown("""
    <style>
    .stButton>button { background-color: #1b5e20; color: white; border-radius: 10px; height: 3em; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border: 2px solid #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# 3. Motor de Generación con Limpieza de Trama
def ejecutar_simulacro_ia(tema, nivel, cantidad):
    instruccion = (
        f"Eres un experto en normativa colombiana y concursos de la CNSC. "
        f"Genera un examen de {cantidad} preguntas sobre '{tema}' para nivel {nivel}. "
        f"Responde SOLO el objeto JSON puro, sin texto adicional, con este formato: "
        f"[{{'p': 'pregunta', 'o': ['A', 'B', 'C'], 'r': 'A', 's': 'sustento legal'}}]"
    )
    try:
        # Llamada de alta prioridad
        response = model.generate_content(instruccion)
        raw_text = response.text.strip()
        
        # Filtro de seguridad para JSON
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_text)
    except Exception as e:
        st.error(f"Falla de Respuesta: El modelo {MODEL_NAME} reporta: {e}")
        return None

# 4. Interfaz de Usuario (Búnker)
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.header("🏆 Búnker de Inteligencia Artificial")

if st.session_state.fase == "inicio":
    st.write("Panel de Generación de Contenido Normativo")
    tema_input = st.text_input("🎯 Ingrese el tema de estudio (Ley, Decreto o Proceso):")
    nivel_sel = st.selectbox("Nivel del Concurso:", ["Asistencial", "Técnico", "Profesional"])
    cant_sel = st.slider("Número de ítems:", 3, 10, 5)
    
    if st.button("🚀 CONSTRUIR SIMULACRO"):
        if tema_input:
            with st.spinner("Procesando normativa y generando preguntas..."):
                data = ejecutar_simulacro_ia(tema_input, nivel_sel, cant_sel)
                if data:
                    st.session_state.preguntas = data
                    st.session_state.tema_actual = tema_input
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("Debe especificar un tema normativo.")

elif st.session_state.fase == "examen":
    st.subheader(f"Evaluación: {st.session_state.tema_actual}")
    for i, item in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {item['p']}**")
        st.radio("Seleccione la opción correcta:", item['o'], key=f"q_{i}", index=None)
        st.write("---")
    
    if st.button("🏁 Finalizar y Retornar"):
        st.session_state.fase = "inicio"
        st.rerun()
