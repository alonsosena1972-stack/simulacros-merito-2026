import streamlit as st
import google.generativeai as genai
import json

# ================= 1. CONEXIÓN DIRECTA =================
# RECUERDA: Genera una nueva llave en Google AI Studio si la anterior sigue fallando
NUEVA_LLAVE = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 

genai.configure(api_key=NUEVA_LLAVE)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide")

# ================= 2. MOTOR DE SIMULACRO (CORREGIDO) =================
def generar_simulacro(tema, nivel):
    # Usamos doble llave {{ }} para que Python no se confunda con el JSON
    prompt = (
        f"Genera 3 preguntas de opción múltiple sobre {tema} para nivel {nivel} en Colombia. "
        f"Responde ÚNICAMENTE un JSON con este formato exacto: "
        f"[{{'p':'pregunta','o':['A','B','C'],'r':'A'}}] "
        f"No escribas nada más que el JSON."
    )
    
    try:
        response = model.generate_content(prompt)
        res_text = response.text.strip()
        
        # Limpieza de etiquetas markdown por seguridad
        if "```" in res_text:
            res_text = res_text.split("```")[1].replace("json", "").strip()
            
        return json.loads(res_text)
    except Exception as e:
        st.error(f"Error de procesamiento: {e}")
        return None

# ================= 3. INTERFAZ PROFESIONAL =================
st.title("🏆 SÍ AL MÉRITO - Búnker IA")
st.markdown("---")

if 'preguntas' not in st.session_state:
    st.subheader("Configuración del Simulacro")
    tema_input = st.text_input("🎯 Tema de estudio (Ej: Ley 1437):")
    nivel_input = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
    
    if st.button("🚀 GENERAR SIMULACRO"):
        if tema_input:
            with st.spinner("⏳ Conectando con la Inteligencia Artificial..."):
                data = generar_simulacro(tema_input, nivel_input)
                if data:
                    st.session_state.preguntas = data
                    st.rerun()
        else:
            st.warning("⚠️ Escribe un tema primero.")
else:
    st.subheader("📝 Resuelve tu examen")
    for i, q in enumerate(st.session_state.preguntas):
        st.write(f"**{i+1}. {q['p']}**")
        st.radio("Selecciona:", q['o'], key=f"p_{i}", index=None)
        st.divider()
    
    if st.button("🔄 Crear nuevo simulacro"):
        del st.session_state.preguntas
        st.rerun()
