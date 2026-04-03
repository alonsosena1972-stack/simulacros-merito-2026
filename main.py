import streamlit as st

# Configuración visual de SÍ AL MÉRITO
st.set_page_config(page_title="SÍ AL MÉRITO: Entrenamiento Pro", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🏆 SÍ AL MÉRITO: Entrenamiento Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Centro de Entrenamiento de Alto Rendimiento para Concursos de Mérito</b></p>", unsafe_allow_html=True)
st.write("---")

# BARRA LATERAL
with st.sidebar:
    st.header("🎯 Configura tu Prueba")
    nivel = st.selectbox("1. Elige tu Nivel:", ["Asistencial", "Técnico", "Profesional", "Profesional Asesor"])

    if nivel == "Asistencial":
        temas = ["Ley 1755 (Peticiones)", "Gestión Documental Básica", "Atención al Ciudadano"]
    elif nivel == "Técnico":
        temas = ["Competencias Comportamentales", "Procesos Administrativos"]
    else:
        temas = ["Régimen Disciplinario", "Ley 1960 (Encargos)", "Contratación Estatal"]

    tema = st.selectbox("2. Elige el Tema:", temas)
    preguntas = st.select_slider("3. Cantidad de preguntas:", options=[10, 20, 50, 100])

    st.write("---")
    iniciar = st.button("🚀 INICIAR ENTRENAMIENTO")

# CUERPO PRINCIPAL
if iniciar:
    if preguntas > 10:
        st.warning("🔒 NIVEL VIP DETECTADO")
        clave = st.text_input("Ingresa tu Código de Estudiante VIP:", type="password")
        if clave == "CESAR2026":
            st.success("¡Bienvenido al Olimpo, César! Generando simulacro de alto impacto...")
            st.info("Cargando preguntas de Juicio Situacional (4 párrafos de contexto)...")
        else:
            st.error("Acceso restringido. Contacta a SÍ AL MÉRITO para obtener tu código.")
    else:
        st.info(f"Iniciando Simulacro Gratuito de 10 preguntas para Nivel {nivel}...")
        st.balloons()
        st.write(f"### Preparando cuestionario sobre {tema}...")
else:
    st.write("### 👤 Bienvenido, Aspirante.")
    st.write("Para comenzar, selecciona tu nivel de carrera y el tema que deseas fortalecer en el panel de la izquierda.")
    st.info("Recuerda: Los simulacros gratuitos son de 10 preguntas. El modo VIP desbloquea hasta 100 preguntas con cronómetro real.")

st.write("---")
st.caption("Powered by SÍ AL MÉRITO - 2026")
