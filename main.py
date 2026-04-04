import streamlit as st
import google.generativeai as genai
import json
import re

# ================= 1. CONFIGURACIÓN DE MOTOR (ALTA COMPATIBILIDAD) =================
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# CAMBIO CLAVE: Se usa la ruta completa del modelo para evitar el Error 404
MODEL_NAME = 'models/gemini-1.5-flash'
model = genai.GenerativeModel(model_name=MODEL_NAME)

# ================= 2. INTERFAZ PROFESIONAL SÍ AL MÉRITO =================
st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { 
        background: linear-gradient(90deg, #1b5e20 0%, #2e7d32 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; border: none;
    }
    .stTextInput>div>div>input { border: 2px solid #1b5e20; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ================= 3. MOTOR DE GENERACIÓN =================
def generar_simulacro_ia(tema, nivel, cantidad):
    prompt = (
        f"Eres un experto en normativa de Colombia y CNSC. Genera un examen de {cantidad} preguntas "
        f"sobre '{tema}' para nivel {nivel}. Responde ÚNICAMENTE un JSON puro: "
        f"[{{'p': 'pregunta', 'o': ['A', 'B', 'C', 'D'], 'r': 'Opción Correcta', 's': 'Sustento Legal'}}]"
    )
    
    try:
        # Petición directa al modelo
        response = model.generate_content(prompt)
        res_text = response.text.strip()

        # Limpiador de tramas JSON para evitar errores de formato
        if "```" in res_text:
            match = re.search(r"\[.*\]", res_text.replace("```json", "").replace("```", ""), re.DOTALL)
            if match:
                res_text = match.group(0)
        
        return json.loads(res_text)
    except Exception as e:
        st.error(f"⚠️ Error Crítico de Servidor: {e}")
        return None

# ================= 4. NAVEGACIÓN =================
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.title("🏆 SÍ AL MÉRITO: Búnker de IA")
st.markdown("---")

if st.session_state.fase == "inicio":
    st.subheader("⚙️ Configuración del Simulacro")
    tema = st.text_input("🎯 Tema Normativo:", placeholder="Ej: Ley 1437, MIPG, Acuerdo CNSC...")
    nivel = st.selectbox("Nivel del Cargo:", ["Asistencial", "Técnico", "Profesional"])
    cantidad = st.slider("Cantidad de preguntas:", 3, 10, 5)
    
    if st.button("🚀 CONSTRUIR SIMULACRO"):
        if tema:
            with st.spinner("⏳ Conectando con el cerebro de la IA..."):
                data = generar_simulacro_ia(tema, nivel, cantidad)
                if data:
                    st.session_state.preguntas = data
                    st.session_state.respuestas_usuario = {}
                    st.session_state.tema_actual = tema
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("⚠️ Debes ingresar un tema.")

elif st.session_state.fase == "examen":
    st.subheader(f"📝 Examen: {st.session_state.tema_actual}")
    
    for i, item in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {item['p']}**")
        opcion = st.radio("Selecciona:", item['o'], key=f"p_{i}", index=None)
        st.session_state.respuestas_usuario[i] = opcion
        st.divider()

    if st.button("📊 FINALIZAR Y CALIFICAR"):
        st.session_state.fase = "resultado"
        st.rerun()

elif st.session_state.fase == "resultado":
    st.header("📊 Resultados")
    # Lógica de calificación simplificada para prueba
    st.success("Simulacro finalizado. Revisa tus respuestas.")
    
    with st.expander("🔍 Ver Retroalimentación"):
        for i, item in enumerate(st.session_state.preguntas):
            st.markdown(f"**{i+1}. {item['p']}**")
            st.write(f"✅ Correcta: {item['r']}")
            st.info(f"⚖️ Sustento: {item['s']}")

    if st.button("🔄 Nuevo Simulacro"):
        st.session_state.fase = "inicio"
        st.rerun()
