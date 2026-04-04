import streamlit as st
import google.generativeai as genai
import json

# 1. Configuración de Seguridad de la API
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# 2. MODELO CORREGIDO (Nombre técnico completo para evitar el Error 404)
# Usamos la versión estable pro que es la más compatible con v1beta
model = genai.GenerativeModel('models/gemini-pro')

st.set_page_config(page_title="SÍ AL MÉRITO - IA Engine", layout="wide")

# Estilo visual de SÍ AL MÉRITO
st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border: 2px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# 3. Función IA con Filtro de Seguridad
def generar_preguntas_ia(tema, nivel, cantidad):
    prompt = (
        f"Genera un examen de {cantidad} preguntas sobre '{tema}' para nivel {nivel} en Colombia. "
        f"Responde ÚNICAMENTE un array JSON con este formato: "
        f"[{{'p': 'pregunta', 'o': ['A', 'B', 'C'], 'r': 'A', 's': 'sustento'}}]"
    )
    try:
        # Generación de contenido
        response = model.generate_content(prompt)
        texto = response.text.strip()
        
        # Limpieza de posibles etiquetas markdown
        if "```json" in texto:
            texto = texto.split("```json")[1].split("```")[0].strip()
        elif "```" in texto:
            texto = texto.split("```")[1].split("```")[0].strip()
            
        return json.loads(texto)
    except Exception as e:
        st.error(f"Error de conexión: El servidor de Google está validando la petición. Reintenta en 10 segundos. (Detalle: {e})")
        return None

# 4. Interfaz del Búnker
if 'fase' not in st.session_state: st.session_state.fase = "inicio"

st.header("🏆 Búnker de Inteligencia Artificial")

if st.session_state.fase == "inicio":
    st.info("Escribe el tema y la IA redactará el simulacro para SÍ AL MÉRITO.")
    tema_input = st.text_input("🎯 ¿Qué tema quieres estudiar hoy?", placeholder="Ej: Ley 1755 de 2015, MIPG...")
    nivel_sel = st.selectbox("Nivel de Carrera:", ["Asistencial", "Técnico", "Profesional"])
    cant_sel = st.slider("Cantidad de preguntas:", 3, 10, 3)
    
    if st.button("✨ GENERAR EXAMEN AHORA"):
        if tema_input:
            with st.spinner("La IA de SÍ AL MÉRITO está redactando tus preguntas..."):
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
        st.radio("Selecciona tu respuesta:", q['o'], key=f"pre_{i}", index=None)
        st.write("---")
    
    if st.button("🏁 Finalizar y Volver"):
        st.session_state.fase = "inicio"
        st.rerun()
