import streamlit as st
import random

# 1. CONFIGURACIÓN PROFESIONAL DE SÍ AL MÉRITO
st.set_page_config(page_title="SÍ AL MÉRITO: Entrenamiento Pro", layout="wide")

# Estilos de marca (Verde y Dorado)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { 
        background-color: #2e7d32; 
        color: white; 
        border-radius: 8px; 
        height: 3em; 
        width: 100%;
        font-weight: bold;
    }
    .stRadio > label { color: #d4af37 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado Principal
st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🏆 SÍ AL MÉRITO: Entrenamiento Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'><b>Centro de Entrenamiento de Alto Rendimiento para Concursos de Mérito</b></p>", unsafe_allow_html=True)
st.write("---")

# 2. BASE DE DATOS DE PREGUNTAS (Aquí puedes seguir agregando más)
# Nota: Asegúrate de que las opciones ('o') incluyan siempre la respuesta correcta ('r')
preguntas_db = {
    "Ley 1755 (Peticiones)": [
        {"p": "¿Cuál es el plazo general para responder una petición de interés general?", "o": ["10 días hábiles", "15 días hábiles", "30 días hábiles"], "r": "15 días hábiles"},
        {"p": "¿Qué plazo hay para responder consultas a las autoridades?", "o": ["10 días", "30 días hábiles", "15 días"], "r": "30 días hábiles"}
    ],
    "Régimen Disciplinario": [
        {"p": "¿Cuál es la sanción máxima para una falta gravísima dolosa?", "o": ["Destitución e inhabilidad", "Suspensión de 1 mes", "Amonestación escrita"], "r": "Destitución e inhabilidad"},
        {"p": "¿A quién se le aplica el Código General Disciplinario?", "o": ["Solo a empleados públicos", "A servidores públicos y particulares que cumplen funciones públicas", "Solo a contratistas"], "r": "A servidores públicos y particulares que cumplen funciones públicas"}
    ]
}

# 3. GESTIÓN DEL ESTADO (La "memoria" de la App)
if 'entrenamiento_iniciado' not in st.session_state:
    st.session_state.entrenamiento_iniciado = False
if 'preguntas_actuales' not in st.session_state:
    st.session_state.preguntas_actuales = []

# 4. PANEL LATERAL (CONFIGURACIÓN)
with st.sidebar:
    st.header("🎯 Panel de Control")
    nivel = st.selectbox("1. Elige tu Nivel:", ["Asistencial", "Técnico", "Profesional"])
    tema = st.selectbox("2. Elige el Tema:", list(preguntas_db.keys()))
    cantidad = st.slider("3. Cantidad de preguntas:", 2, 20, 5)
    
    if st.button("🚀 INICIAR ENTRENAMIENTO"):
        # Seleccionamos preguntas al azar del tema elegido
        lista_tema = preguntas_db[tema]
        n_seleccionar = min(len(lista_tema), cantidad)
        st.session_state.preguntas_actuales = random.sample(lista_tema, n_seleccionar)
        st.session_state.entrenamiento_iniciado = True
        st.session_state.respuestas_usuario = {} # Limpiamos respuestas anteriores

# 5. ÁREA DE EXAMEN
if st.session_state.entrenamiento_iniciado:
    st.subheader(f"📝 Simulacro: {tema} ({nivel})")
    
    # Formulario para evitar que la página se refresque con cada clic
    with st.form("examen_form"):
        for i, item in enumerate(st.session_state.preguntas_actuales):
            st.markdown(f"**Pregunta {i+1}:** {item['p']}")
            st.session_state.respuestas_usuario[i] = st.radio(
                "Selecciona una opción:", 
                item['o'], 
                key=f"q_{i}_{tema}"
            )
            st.write("") # Espacio
        
        boton_finalizar = st.form_submit_button("✅ FINALIZAR Y CALIFICAR")
        
        if boton_finalizar:
            aciertos = 0
            for i, item in enumerate(st.session_state.preguntas_actuales):
                if st.session_state.respuestas_usuario[i] == item['r']:
                    aciertos += 1
            
            # Resultado Final
            st.balloons()
            st.markdown(f"### Resultado: {aciertos} / {len(st.session_state.preguntas_actuales)} correctas")
            if aciertos == len(st.session_state.preguntas_actuales):
                st.success("¡Puntaje Perfecto! Estás listo para el mérito. 🏆")
            else:
                st.info("Sigue practicando para alcanzar la excelencia.")

else:
    st.warning("👈 Por favor, configura tu prueba en el panel de la izquierda y presiona 'Iniciar Entrenamiento'.")

st.write("---")
st.caption("Desarrollado por SÍ AL MÉRITO - 2026")
