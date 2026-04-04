import streamlit as st
import google.generativeai as genai
import json

# 1. Configuración de tu llave (Directa)
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# 2. Definición del Modelo (Sin procesos extra para evitar PermissionDenied)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="SÍ AL MÉRITO - IA Engine", layout="wide")

# Estilo visual de SÍ AL MÉRITO
st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border: 2px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# 3. Función de Generación de Preguntas
def generar_preguntas_ia(tema, nivel, cantidad):
    prompt = (
        f"Genera un examen de {cantidad} preguntas sobre '{tema}' para nivel {nivel} en Colombia. "
        f"Responde ÚNICAMENTE un array JSON con este formato: "
        f"[{{'p': 'pregunta', 'o': ['A', 'B', 'C'], 'r': 'A', 's': 'sustento'}}]"
    )
    try:
        response = model.generate_content(prompt)
        texto = response.text.strip()
        # Limpieza de etiquetas markdown si aparecen
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0].strip()
        return json.loads(texto)
    except Exception as e:
        st.error(f"Error de acceso: Asegúrate de que la API Key esté activa en Google AI Studio. (Detalle: {e})")
        return None

# 4. Interfaz del Búnker
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.header("🏆 Búnker de Inteligencia Artificial")

if st.session_state.fase == "inicio":
    st.info("Escribe el tema y la IA redactará el simulacro para SÍ AL MÉRITO.")
    tema_input = st.text_input("🎯 ¿Qué tema quieres estudiar hoy?", placeholder="Ej: Ley 1755 de 2015...")
    nivel_sel = st.selectbox("Nivel de Carrera:", ["Asistencial", "Técnico", "Profesional"])
    cant_sel = st.slider("Cantidad de preguntas:", 3, 10, 3)
    
    if st.button("🚀 GENERAR EXAMEN AHORA"):
        if tema_input:
            with st.spinner("La IA de SÍ AL MÉRITO está redactando..."):
                resultado = generar_preguntas_ia(tema_input, nivel_sel, cant_sel)
                if resultado:
                    st.session_state.preguntas = resultado
                    st.session_state.tema_actual = tema_input
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("Por favor, escribe un tema.")

elif st.session_state.fase == "examen":
    st.subheader(f"Simulacro: {st.session_state.tema_actual}")
    for i, q in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {q['p']}**")
        st.radio("Respuesta:", q['o'], key=f"r_{i}", index=None)
        st.write("---")
    
    if st.button("🏁 Volver al Inicio"):
        st.session_state.fase = "inicio"
        st.rerun()
