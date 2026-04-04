import streamlit as st
import google.generativeai as genai
import json
import os
import re

# ================= CONFIGURACIÓN SEGURA =================
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    st.error("⚠️ Debes configurar la variable de entorno GENAI_API_KEY")
    st.stop()

# Configurar API
genai.configure(api_key=GENAI_API_KEY)

# Modelo actualizado y funcional
model = genai.GenerativeModel('gemini-1.5-flash')

# ================= CONFIG UI =================
st.set_page_config(page_title="SÍ AL MÉRITO - Simulador IA", layout="wide")

st.markdown("""
    <style>
    .stButton>button { background-color: #1b5e20; color: white; border-radius: 10px; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { border: 2px solid #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

# ================= FUNCIÓN PRINCIPAL =================
def generar_simulacro(tema, nivel, cantidad):
    prompt = (
        f"Genera un cuestionario de {cantidad} preguntas sobre '{tema}' para nivel {nivel} en Colombia. "
        f"Devuelve SOLO un JSON válido (sin texto adicional) con este formato: "
        f"[{'{'}\"p\": \"pregunta\", \"o\": [\"A\", \"B\", \"C\", \"D\"], \"r\": \"A\", \"s\": \"sustento\"{'}'}]"
    )

    try:
        response = model.generate_content(prompt)
        res_text = response.text.strip()

        # Limpiar bloques markdown
        if "```" in res_text:
            res_text = res_text.split("```")[1].replace("json", "").strip()

        # Extraer JSON aunque venga con texto adicional
        match = re.search(r"\[.*\]", res_text, re.DOTALL)
        if match:
            res_text = match.group(0)

        data = json.loads(res_text)
        return data

    except Exception as e:
        st.error(f"❌ Error procesando la respuesta: {e}")
        return None

# ================= ESTADO =================
if 'fase' not in st.session_state:
    st.session_state.fase = "inicio"

# ================= INTERFAZ =================
st.header("🏆 SÍ AL MÉRITO - Simulador Inteligente")

if st.session_state.fase == "inicio":
    st.subheader("Configuración del simulacro")

    tema = st.text_input("🎯 Tema:")
    nivel = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
    cantidad = st.slider("Número de preguntas:", 3, 15, 5)

    if st.button("🚀 Generar Simulacro"):
        if tema:
            with st.spinner("Generando preguntas..."):
                data = generar_simulacro(tema, nivel, cantidad)

                if data:
                    st.session_state.preguntas = data
                    st.session_state.respuestas = {}
                    st.session_state.tema = tema
                    st.session_state.fase = "examen"
                    st.rerun()
        else:
            st.warning("⚠️ Debes ingresar un tema")

# ================= EXAMEN =================
elif st.session_state.fase == "examen":
    st.subheader(f"Simulacro: {st.session_state.tema}")

    for i, item in enumerate(st.session_state.preguntas):
        st.markdown(f"**{i+1}. {item['p']}**")

        respuesta = st.radio(
            "Seleccione una opción:",
            item['o'],
            key=f"q_{i}",
            index=None
        )

        st.session_state.respuestas[i] = respuesta

    if st.button("📊 Calificar"):
        correctas = 0

        for i, item in enumerate(st.session_state.preguntas):
            if st.session_state.respuestas.get(i) == item['r']:
                correctas += 1

        total = len(st.session_state.preguntas)
        score = (correctas / total) * 100

        st.success(f"✅ Resultado: {correctas}/{total} ({score:.2f}%)")

        with st.expander("📘 Ver respuestas correctas"):
            for i, item in enumerate(st.session_state.preguntas):
                st.markdown(f"**{i+1}. {item['p']}**")
                st.write(f"✔ Correcta: {item['r']}")
                st.write(f"🧠 Sustento: {item['s']}")
                st.markdown("---")

    if st.button("🔄 Nuevo simulacro"):
        st.session_state.fase = "inicio"
        st.rerun()
