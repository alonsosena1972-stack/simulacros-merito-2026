import streamlit as st
import google.generativeai as genai
import json

# ================= 1. NUEVA CONEXIÓN =================
# REEMPLAZA ESTA LLAVE POR LA NUEVA QUE CREASTE
NUEVA_LLAVE = "AIzaSyCsJESVFAfjbp8yi3PZYGebD_EESV2oQro" 

genai.configure(api_key=NUEVA_LLAVE)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide")

# ================= 2. MOTOR DE SIMULACRO =================
def generar_simulacro(tema, nivel):
    prompt = f"Genera 3 preguntas de opción múltiple sobre {tema} para nivel {nivel} en Colombia. Responde SOLO un JSON: [{'p':'...','o':['A','B','C'],'r':'A'}]"
    try:
        response = model.generate_content(prompt)
        # Limpieza rápida de la respuesta
        texto = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(texto)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# ================= 3. INTERFAZ MÍNIMA PARA PRUEBA =================
st.title("🏆 SÍ AL MÉRITO - Búnker IA")

if 'preguntas' not in st.session_state:
    tema = st.text_input("🎯 ¿Qué tema probamos?")
    nivel = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
    
    if st.button("🚀 PROBAR CONEXIÓN"):
        with st.spinner("Conectando..."):
            data = generar_simulacro(tema, nivel)
            if data:
                st.session_state.preguntas = data
                st.rerun()
else:
    for i, q in enumerate(st.session_state.preguntas):
        st.write(f"**{i+1}. {q['p']}**")
        st.radio("Opciones:", q['o'], key=f"p_{i}")
    
    if st.button("🔄 Reiniciar"):
        del st.session_state.preguntas
        st.rerun()
