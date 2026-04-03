import streamlit as st
import google.generativeai as genai
import json

# 1. CONFIGURACIÓN DE LA LLAVE (Tu llave personal)
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# 2. SELECCIÓN DEL MODELO (Línea corregida para evitar error 404)
model = genai.GenerativeModel(''gemini-1.5-flash'')

# 3. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="SÍ AL MÉRITO - IA Engine", layout="wide")

st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; }
    .stTextInput>div>div>input { border: 2px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# 4. FUNCIÓN PARA GENERAR PREGUNTAS (En inglés técnico)
def generar_preguntas_ia(tema, nivel, cantidad):
    prompt = f"Actúa como experto en la CNSC de Colombia. Genera un examen de {cantidad} preguntas sobre el tema '{tema}' para nivel {nivel}. Responde ÚNICAMENTE en formato JSON: [{{'p': 'pregunta', 'o': ['A', 'B', 'C'], 'r': 'A', 's': 'sustento legal'}}]"
    try:
        response = model.generate_content(prompt)
        # Limpieza de la respuesta para obtener solo el JSON
        texto_limpio = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(texto_limpio)
    except Exception as e:
        st.error(f"Error al conectar con la IA: {e}")
        return None

# 5. LÓGICA DE NAVEGACIÓN
if 'fase' not in st.session_state:
    st.session_state.fase = "inicio"

st.header("🏆 Búnker de Inteligencia Artificial")

if st.session_state.fase == "inicio":
    st.write("Escribe el tema y la IA redactará el simulacro basado en la normativa vigente.")
    tema_input = st.text_input("🎯 ¿Qué tema quieres estudiar hoy?", placeholder="Ej: Ley 1474 de 2011, MIPG, Atención al ciudadano...")
    nivel_sel = st.selectbox("Nivel de Carrera:", ["Asistencial", "Técnico", "Profesional"])
    cant_sel = st.slider("Cantidad de preguntas:", 3, 10, 5)
    
    if st.button("🚀 GENERAR EXAMEN AHORA"):
        if tema_input:
            with st.spinner("La IA de SÍ AL MÉRITO está redactando tus preguntas..."):
                resultado = generar_preguntas_ia(tema_input, nivel_sel, cant_sel)
                if resultado:
                    st.session_state.preguntas = resultado
                    st.session_state.tema_actual = tema_input
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("Por favor, digita un tema primero.")

elif st.session_state.fase == "examen":
    st.subheader(f"Simulacro: {st.session_state.tema_actual}")
    
    for i, q in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {q['p']}**")
        st.radio("Selecciona tu respuesta:", q['o'], key=f"ia_p_{i}")
        st.write("---")
    
    if st.button("🏁 Finalizar y Volver al Inicio"):
        st.session_state.fase = "inicio"
        st.rerun()
