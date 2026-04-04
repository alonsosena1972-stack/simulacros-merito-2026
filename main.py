import streamlit as st
import google.generativeai as genai
import json

# ================= 1. CONEXIÓN INTELIGENTE =================
# Si esta llave sigue fallando, genera una NUEVA en AI Studio, es vital.
API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=API_KEY)

@st.cache_resource
def configurar_modelo():
    try:
        # Buscamos qué modelos tiene tu cuenta permitidos actualmente
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Intentamos usar el más moderno que encuentre, si no, el primero de la lista
        seleccionado = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in modelos else modelos[0]
        return genai.GenerativeModel(seleccionado)
    except Exception as e:
        st.error(f"Error crítico de configuración: {e}")
        return None

model = configurar_modelo()

# ================= 2. MOTOR DEL BÚNKER =================
def generar_simulacro(tema, nivel):
    # Prompt blindado contra errores de llaves de Python
    prompt = (
        f"Genera 3 preguntas de opción múltiple sobre {tema} para nivel {nivel} en Colombia. "
        f"Responde ÚNICAMENTE un JSON con este formato: "
        f"[{{\"p\":\"pregunta\",\"o\":[\"A\",\"B\",\"C\"],\"r\":\"A\"}}]"
    )
    
    try:
        response = model.generate_content(prompt)
        res_text = response.text.strip()
        
        # Limpiador de etiquetas markdown
        if "```" in res_text:
            res_text = res_text.split("```")[1].replace("json", "").strip()
            
        return json.loads(res_text)
    except Exception as e:
        st.error(f"La IA no pudo responder: {e}")
        return None

# ================= 3. INTERFAZ SÍ AL MÉRITO =================
st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide")
st.title("🏆 SÍ AL MÉRITO - Búnker IA")
st.markdown("---")

if model is None:
    st.error("⚠️ No se detectaron modelos disponibles. Por favor, revisa tu API Key en Google AI Studio.")
    st.stop()

if 'preguntas' not in st.session_state:
    st.subheader("Configuración del Simulacro")
    tema_input = st.text_input("🎯 Tema (Ej: Ley 1437 de 2011):")
    nivel_input = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
    
    if st.button("🚀 GENERAR SIMULACRO"):
        if tema_input:
            with st.spinner("⏳ Buscando modelos compatibles y generando preguntas..."):
                data = generar_simulacro(tema_input, nivel_input)
                if data:
                    st.session_state.preguntas = data
                    st.rerun()
else:
    st.subheader("📝 Examen Generado")
    for i, q in enumerate(st.session_state.preguntas):
        st.write(f"**{i+1}. {q['p']}**")
        st.radio("Opciones:", q['o'], key=f"p_{i}", index=None)
        st.divider()
    
    if st.button("🔄 Nuevo examen"):
        del st.session_state.preguntas
        st.rerun()
