import streamlit as st
import google.generativeai as genai
import json

# 1. Configuración de tu Llave
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# 2. Definición del Modelo (Línea 11 corregida)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="SÍ AL MÉRITO - IA Engine", layout="wide")

# 3. Función para generar preguntas
def generar_preguntas_ia(tema, nivel, cantidad):
    prompt = f"Actúa como experto en la CNSC de Colombia. Genera un examen de {cantidad} preguntas sobre el tema '{tema}' para nivel {nivel}. Responde ÚNICAMENTE en formato JSON: [{{'p': 'pregunta', 'o': ['A', 'B', 'C'], 'r': 'A', 's': 'sustento legal'}}]"
    try:
        response = model.generate_content(prompt)
        texto_limpio = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(texto_limpio)
    except Exception as e:
        st.error(f"Error al generar: {e}")
        return None

# 4. Control de la Aplicación
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.header("🏆 Búnker de Inteligencia Artificial")

if st.session_state.fase == "inicio":
    st.write("Escribe el tema y la IA redactará el simulacro.")
    tema_input = st.text_input("🎯 ¿Qué tema quieres estudiar hoy?")
    nivel_sel = st.selectbox("Nivel de Carrera:", ["Asistencial", "Técnico", "Profesional"])
    cant_sel = st.slider("Cantidad de preguntas:", 3, 10, 5)
    
    if st.button("🚀 GENERAR EXAMEN AHORA"):
        if tema_input:
            with st.spinner("La IA está trabajando para ti..."):
                preguntas = generar_preguntas_ia(tema_input, nivel_sel, cant_sel)
                if preguntas:
                    st.session_state.preguntas = preguntas
                    st.session_state.tema_actual = tema_input
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("Escribe un tema primero.")

elif st.session_state.fase == "examen":
    st.subheader(f"Simulacro: {st.session_state.tema_actual}")
    for i, q in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {q['p']}**")
        st.radio("Selecciona tu respuesta:", q['o'], key=f"pregunta_{i}")
        st.write("---")
    
    if st.button("🏁 Finalizar y Volver"):
        st.session_state.fase = "inicio"
        st.rerun()
