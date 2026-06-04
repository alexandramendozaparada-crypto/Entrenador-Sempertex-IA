import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name='gemini-2.5-flash')

# 1. Definimos los nombres exactos de tus archivos
VIDEO_SAP = "Introducción a SAP_ El ERP Líder_1080p.mp4"
VIDEO_MODULOMMSAP = "introduccion-a-sap-modulo-mm-1080p-caption.mp4"
VIDEO_BIENVENIDA = "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"

st.title("🏭 Entrenador IA - Sempertex")

# Inicializar estado
if 'video_actual' not in st.session_state:
    st.session_state.video_actual = VIDEO_BIENVENIDA
    st.session_state.texto = "¡Bienvenido! ¿Cómo puedo ayudarte hoy?"

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

if user_input:
    with st.spinner('Analizando consulta...'):
        # Clasificación forzada
        prompt = f"Clasifica la intención de esta pregunta: '{user_input}'. Responde SOLO con una de estas tres palabras: 'sap', 'maquinaria' o 'bienvenida'."
        categoria = model.generate_content(prompt).text.strip().lower()
        
        # Lógica explícita (Más segura que el diccionario)
        if 'sap' in categoria:
            st.session_state.video_actual = VIDEO_SAP
        elif 'maquinaria' in categoria:
            st.session_state.video_actual = VIDEO_MAQUINARIA
        else:
            st.session_state.video_actual = VIDEO_BIENVENIDA
            
        st.session_state.texto = model.generate_content(f"Saluda brevemente sobre: {user_input}").text

# Renderizado
col1, col2 = st.columns(2)
with col1:
    st.subheader("Mentor Virtual")
    st.video(st.session_state.video_actual)

with col2:
    st.subheader("Introducción")
    st.write(st.session_state.texto)
