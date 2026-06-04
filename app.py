import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name='gemini-2.5-flash')

# 1. Nombres exactos de tus archivos de video
VIDEOS = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "mm": "introduccion-a-sap-modulo-mm-1080p-caption.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# 2. Lógica de selección con prioridad
input_lower = user_input.lower()
video_actual = VIDEOS["bienvenida"]
texto_actual = "¡Bienvenido! ¿Cómo puedo ayudarte hoy?"

if user_input:
    # Prioridad: Si menciona 'mm', va directo al video de MM
    if 'mm' in input_lower:
        video_actual = VIDEOS["mm"]
        tema_ia = "el módulo SAP MM"
    # Si menciona 'sap' (pero no 'mm'), va al video general de SAP
    elif 'sap' in input_lower:
        video_actual = VIDEOS["sap"]
        tema_ia = "SAP"
    # Default
    else:
        video_actual = VIDEOS["bienvenida"]
        tema_ia = user_input
    
    texto_actual = model.generate_content(f"Saluda y presenta brevemente el tema: {tema_ia}").text

# 3. Renderizado
col1, col2 = st.columns(2)
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_actual)
with col2:
    st.subheader("Introducción")
    st.write(texto_actual)
