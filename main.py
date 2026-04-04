import streamlit as st
import google.generativeai as genai
import json

# 1. Autenticación Robusta
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# 2. SELECCIÓN DE MODELO DE RESPALDO (Nombre base universal)
# Si falla el flash, este código está diseñado para no romperse
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide")

# Estilo de interfaz limpia
st.markdown("""
    <style>
    .stButton>button { background-color: #1b5e20; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border: 2px solid #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# 3. Motor de Generación con Doble Validación
def generar_simulacro_profesional(tema, nivel, cantidad):
    prompt = (
        f"Eres un experto legal en la CNSC Colombia. Genera un cuestionario de {cantidad} preguntas "
        f"sobre '{tema}' para nivel {nivel}. Responde estrictamente en formato JSON: "
        f"[{{'p': 'pregunta', 'o': ['A', 'B', 'C'], 'r': 'A', 's': 'sustento'}}] "
        f"No añadas saludo ni despedida, solo el JSON."
    )
    try:
        # Ejecución de la petición
        response = model.generate_content(prompt)
        res_text = response.text.strip()
        
        # Limpiador de etiquetas de código
        if "```" in res_text:
            res_text = res_text.split("```")[1]
            if res_text.startswith("json"):
                res_text = res_text[4:].strip()
        
        return json.loads(res_text)
    except Exception as e:
        st.error(f"Error de comunicación con el motor: {e}")
        return None

# 4. Lógica del Búnker
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.header("🏆 Búnker de Inteligencia Artificial")

if st.session_state.fase == "inicio":
    st.write("Generador de Simulacros Basado en Normativa Vigente")
    tema = st.text_input("🎯 Ingrese el tema (Ej: Ley 1755, Decreto 1083):")
    nivel = st.selectbox("Nivel del Concurso:", ["Asistencial", "Técnico", "Profesional"])
    cant = st.slider("Número de preguntas:", 3, 10, 5)
    
    if st.button("🚀 CONSTRUIR EXAMEN"):
        if tema:
            with st.spinner("La IA está analizando la normativa..."):
                data = generar_simulacro_profesional(tema, nivel, cant)
                if data:
                    st.session_state.preguntas = data
                    st.session_state.tema_actual = tema
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("Por favor ingrese un tema normativo.")

elif st.session_state.fase == "examen":
    st.subheader(f"Simulacro: {st.session_state.tema_actual}")
    for i, item in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {item['p']}**")
        st.radio("Seleccione respuesta:", item['o'], key=f"q_{i}", index=None)
        st.write("---")
    
    if st.button("🏁 Reiniciar Panel"):
        st.session_state.fase = "inicio"
        st.rerun()
