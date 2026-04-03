import streamlit as st
import random
from fpdf import FPDF

# 1. CONFIGURACIÓN DE MARCA "SÍ AL MÉRITO"
st.set_page_config(page_title="SÍ AL MÉRITO - Entrenamiento Pro", layout="wide")

# 2. LÓGICA DE GENERACIÓN DE PDF (EXCLUSIVO VIP)
def crear_pdf(puntaje, resultados, nivel, tema):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(46, 125, 50) # Verde institucional
    pdf.cell(200, 10, "SÍ AL MÉRITO - REPORTE DE ENTRENAMIENTO", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, f"Nivel: {nivel} | Eje: {tema}", ln=True)
    pdf.cell(200, 10, f"Puntaje Final: {puntaje}/100", ln=True)
    pdf.ln(5)
    
    for i, res in enumerate(resultados):
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 8, f"{i+1}. {res['p']}")
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, f"Tu respuesta: {res['u']} | Correcta: {res['c']}", ln=True)
        pdf.set_font("Arial", 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 8, f"Sustento Legal: {res['s']}")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)
    return pdf.output(dest='S').encode('latin-1')

# 3. BANCO DE PREGUNTAS (ORGANIZADO POR NIVEL Y TEMA)
# César: Aquí puedes alimentar el sistema con cientos de preguntas.
preguntas_db = {
    "Profesional": {
        "Gestión Documental": [
            {"p": "¿Qué es un fondo acumulado?", "o": ["Documentos sin criterio", "Archivo histórico", "Bodega"], "r": "Documentos sin criterio", "s": "Según el AGN, son documentos reunidos sin criterios archivísticos."},
            {"p": "¿Cuál es el tiempo máximo de retención en archivo de gestión?", "o": ["5 años", "Según TRD", "10 años"], "r": "Según TRD", "s": "La Tabla de Retención Documental (TRD) define los tiempos según el ciclo vital."},
        ],
        "Ley 1755 (Peticiones)": [
            {"p": "¿Cuál es el plazo para responder peticiones de información?", "o": ["10 días", "15 días", "30 días"], "r": "10 días", "s": "Art. 14 de la Ley 1755 de 2015."},
            {"p": "¿Qué término tiene la autoridad para responder consultas?", "o": ["15 días", "30 días", "10 días"], "r": "30 días", "s": "La Ley 1755 establece 30 días para consultas sobre materias a su cargo."}
        ]
    },
    "Técnico": {
        "Procesos Administrativos": [
            {"p": "¿Cómo se deben foliar los documentos en el archivo?", "o": ["Lápiz de mina negra", "Esfero rojo", "No se folian"], "r": "Lápiz de mina negra", "s": "Acuerdo 042 del AGN (Foliación documental)."},
        ]
    },
    "Asistencial": {
        "Atención al Ciudadano": [
            {"p": "¿Qué es la calidez en el servicio público?", "o": ["Trato amable y cordial", "Rapidez extrema", "Dar obsequios"], "r": "Trato amable y cordial", "s": "Protocolos de Servicio al Ciudadano de la Función Pública."},
        ]
    }
}

# 4. INICIALIZACIÓN DE VARIABLES DE SESIÓN
if 'preguntas' not in st.session_state: st.session_state.preguntas = []
if 'examen_terminado' not in st.session_state: st.session_state.examen_terminado = False
if 'es_vip' not in st.session_state: st.session_state.es_vip = False
if 'respuestas_usuario' not in st.session_state: st.session_state.respuestas_usuario = {}

# 5. PANEL LATERAL (CONFIGURACIÓN)
with st.sidebar:
    st.markdown("## 🏆 SÍ AL MÉRITO")
    codigo = st.text_input("Código Estudiante VIP:", type="password")
    if codigo == "CESAR2026": 
        st.session_state.es_vip = True
        st.success("💎 ACCESO VIP ACTIVADO")
    
    # Filtro de Niveles
    nivel_sel = st.selectbox("1. Selecciona tu Nivel:", list(preguntas_db.keys()))
    # Filtro de Temas según el nivel
    tema_sel = st.selectbox("2. Selecciona el Tema:", list(preguntas_db[nivel_sel].keys()))
    
    cant_max = len(preguntas_db[nivel_sel][tema_sel])
    # Regla VIP: Si es VIP puede elegir hasta 100, si no, solo lo que haya disponible hasta 15
    cantidad = st.slider("3. Cantidad de preguntas:", 1, cant_max, min(10, cant_max))

    if st.button("🚀 INICIAR ENTRENAMIENTO"):
        # Limpiamos todo para el nuevo examen
        st.session_state.preguntas = random.sample(preguntas_db[nivel_sel][tema_sel], cantidad)
        st.session_state.respuestas_usuario = {}
        st.session_state.examen_terminado = False
        st.session_state.nivel_actual = nivel_sel
        st.session_state.tema_actual = tema_sel
        st.rerun()

# 6. CUERPO PRINCIPAL
st.markdown(f"<h1 style='color: #2e7d32;'>SÍ AL MÉRITO: Centro de Entrenamiento</h1>", unsafe_allow_html=True)

if st.session_state.preguntas and not st.session_state.examen_terminado:
    st.info(f"📋 **Nivel:** {st.session_state.nivel_actual} | **Eje:** {st.session_state.tema_actual}")
    
    # Cuestionario en Formulario para evitar recargas molestas
    with st.form("examen_form"):
        for i, q in enumerate(st.session_state.preguntas):
            st.markdown(f"#### Pregunta {i+1}")
            st.write(q['p'])
            # index=None hace que la pregunta empiece VACÍA (sin respuesta marcada)
            st.session_state.respuestas_usuario[i] = st.radio(
                "Selecciona una opción:", 
                q['o'], 
                key=f"p_{i}", 
                index=None
            )
            st.write("---")
        
        btn_finalizar = st.form_submit_button("🏁 FINALIZAR Y CALIFICAR")
        
        if btn_finalizar:
            # Verificar que no falten respuestas
            if None in st.session_state.respuestas_usuario.values():
                st.warning("⚠️ Debes responder todas las preguntas antes de finalizar.")
            else:
                st.session_state.examen_terminado = True
                st.rerun()

# 7. PANTALLA DE RESULTADOS
if st.session_state.examen_terminado:
    correctas = sum(1 for i, q in enumerate(st.session_state.preguntas) if st.session_state.respuestas_usuario[i] == q['r'])
    puntaje = int((correctas / len(st.session_state.preguntas)) * 100)
    
    st.success(f"## Tu Puntaje: {puntaje} / 100")
    
    # Mostrar corrección en pantalla
    for i, q in enumerate(st.session_state.preguntas):
        es_correcta = st.session_state.respuestas_usuario[i] == q['r']
        with st.expander(f"Pregunta {i+1}: {'✅ CORRECTA' if es_correcta else '❌ INCORRECTA'}"):
            st.write(f"**Tu respuesta:** {st.session_state.respuestas_usuario[i]}")
            st.write(f"**Respuesta correcta:** {q['r']}")
            st.info(f"**Sustento Legal:** {q['s']}")

    # Lógica de Extracción PDF (Solo VIP)
    if st.session_state.es_vip:
        st.balloons()
        # Preparar datos para el PDF
        lista_pdf = []
        for i, q in enumerate(st.session_state.preguntas):
            lista_pdf.append({
                'p': q['p'], 
                'u': st.session_state.respuestas_usuario[i], 
                'c': q['r'], 
                's': q['s']
            })
        
        pdf_output = crear_pdf(puntaje, lista_pdf, st.session_state.nivel_actual, st.session_state.tema_actual)
        st.download_button(
            label="📥 DESCARGAR REPORTE PDF",
            data=pdf_output,
            file_name=f"Resultado_{st.session_state.tema_actual}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Acceso Público: Solo puedes ver el puntaje. Los usuarios VIP pueden descargar el reporte con sustento legal.")

# Si no hay examen iniciado, mostrar mensaje de bienvenida
elif not st.session_state.preguntas:
    st.markdown("""
    ### Bienvenido, Aspirante.
    Para comenzar tu entrenamiento, sigue estos pasos:
    1. **Selecciona tu Nivel** en el panel de la izquierda.
    2. **Elige el Eje Temático** que deseas fortalecer.
    3. Haz clic en **Iniciar Entrenamiento**.
    """)
