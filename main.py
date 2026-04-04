import streamlit as st
import google.generativeai as genai
import json
import re

# ================= 1. CONFIGURACIÓN DE MOTOR (CORREGIDA) =================
# He puesto la llave directa para evitar el error de variable de entorno
GENAI_API_KEY = "AIzaSyAv_BfMaM6-jhk1zaCvcUR1z3_cpxDHeqE" 
genai.configure(api_key=GENAI_API_KEY)

# Usamos el modelo más estable para Streamlit Cloud
model = genai.GenerativeModel('gemini-1.5-flash')

# ================= 2. INTERFAZ PROFESIONAL =================
st.set_page_config(page_title="SÍ AL MÉRITO - Búnker IA", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        background: linear-gradient(90deg, #1b5e20 0%, #2e7d32 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 4px 15px rgba(0,0,0,0.2); }
    .stTextInput>div>div>input { border: 2px solid #1b5e20; border-radius: 10px; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# ================= 3. LÓGICA DE ALTA DISPONIBILIDAD =================
def generar_simulacro_ia(tema, nivel, cantidad):
    prompt = (
        f"Eres un experto en leyes de Colombia y concursos CNSC. Genera un examen de {cantidad} preguntas "
        f"sobre '{tema}' para nivel {nivel}. Responde ÚNICAMENTE un JSON puro, sin texto extra, "
        f"con este formato: [{{'p': 'pregunta', 'o': ['A', 'B', 'C', 'D'], 'r': 'La opción exacta escrita igual', 's': 'sustento legal'}}]"
    )
    
    try:
        response = model.generate_content(prompt)
        res_text = response.text.strip()

        # Limpiador de código Markdown (Bypass de errores)
        if "```" in res_text:
            res_text = re.search(r"\[.*\]", res_text.replace("```json", "").replace("```", ""), re.DOTALL).group(0)
        
        return json.loads(res_text)
    except Exception as e:
        st.error(f"⚠️ Error de Conexión IA: {e}")
        return None

# ================= 4. FLUJO DE NAVEGACIÓN =================
if 'fase' not in st.session_state: st.session_state.fase = "inicio"
if 'preguntas' not in st.session_state: st.session_state.preguntas = []

st.title("🏆 SÍ AL MÉRITO: Búnker de IA")
st.markdown("---")

if st.session_state.fase == "inicio":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Configuración del Simulacro")
        tema = st.text_input("🎯 Tema Normativo:", placeholder="Ej: Ley 1437, MIPG, Código de Policía...")
        nivel = st.selectbox("Nivel del Cargo:", ["Asistencial", "Técnico", "Profesional"])
        cantidad = st.select_slider("Cantidad de preguntas:", options=[3, 5, 10, 15], value=5)
        
        if st.button("🚀 GENERAR EXAMEN AHORA"):
            if tema:
                with st.spinner("⏳ La IA está analizando la normativa y redactando..."):
                    data = generar_simulacro_ia(tema, nivel, cantidad)
                    if data:
                        st.session_state.preguntas = data
                        st.session_state.respuestas_usuario = {}
                        st.session_state.tema_actual = tema
                        st.session_state.fase = "examen"
                        st.rerun()
            else:
                st.warning("⚠️ Por favor, ingresa un tema de estudio.")
    
    with col2:
        st.info("""
        **¿Cómo funciona?**
        1. Ingresa la ley o tema que quieres estudiar.
        2. La IA genera preguntas tipo Juicio Situacional (CNSC).
        3. Recibes calificación y sustento legal inmediato.
        """)

elif st.session_state.fase == "examen":
    st.subheader(f"📝 Evaluando: {st.session_state.tema_actual}")
    
    # Mostrar preguntas
    for i, item in enumerate(st.session_state.preguntas):
        with st.container():
            st.markdown(f"#### {i+1}. {item['p']}")
            opcion = st.radio("Selecciona tu respuesta:", item['o'], key=f"pregunta_{i}", index=None)
            st.session_state.respuestas_usuario[i] = opcion
            st.markdown("---")

    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        if st.button("📊 FINALIZAR Y CALIFICAR"):
            st.session_state.fase = "resultado"
            st.rerun()
    with col_fin2:
        if st.button("🔄 CANCELAR"):
            st.session_state.fase = "inicio"
            st.rerun()

elif st.session_state.fase == "resultado":
    st.subheader("📊 Resultados del Simulacro")
    
    correctas = 0
    total = len(st.session_state.preguntas)
    
    for i, item in enumerate(st.session_state.preguntas):
        if st.session_state.respuestas_usuario.get(i) == item['r']:
            correctas += 1
            
    score = (correctas / total) * 100
    
    # Mostrar métricas
    m1, m2 = st.columns(2)
    m1.metric("Puntaje", f"{score:.1f}%")
    m2.metric("Correctas", f"{correctas} de {total}")

    if score >= 70:
        st.balloons()
        st.success("¡Excelente nivel! Estás listo para el concurso.")
    else:
        st.warning("Sigue practicando. Repasa los sustentos legales abajo.")

    with st.expander("🔍 REVISIÓN DETALLADA (Retroalimentación)"):
        for i, item in enumerate(st.session_state.preguntas):
            st.markdown(f"**Pregunta {i+1}:** {item['p']}")
            st.write(f"✅ **Correcta:** {item['r']}")
            st.write(f"❌ **Tu respuesta:** {st.session_state.respuestas_usuario.get(i)}")
            st.info(f"⚖️ **Sustento Legal:** {item['s']}")
            st.markdown("---")

    if st.button("🔄 REALIZAR OTRO EXAMEN"):
        st.session_state.fase = "inicio"
        st.rerun()
