import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name='gemini-2.5-flash')

# 1. Archivos (Nombres exactos)
VIDEOS = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# 2. Lógica simple sin bucles
user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# Valores por defecto
video_actual = VIDEOS["bienvenida"]
texto_actual = "¡Bienvenido! ¿Cómo puedo ayudarte hoy?"

if user_input:
    # Clasificación rápida
    prompt = f"De las opciones: 'sap', 'maquinaria', 'bienvenida'. ¿A qué pertenece: '{user_input}'? Solo responde la palabra."
    cat = model.generate_content(prompt).text.strip().lower()
    
    # Asignación directa
    if 'sap' in cat:
        video_actual = VIDEOS["sap"]
    elif 'maquinaria' in cat or 'mm' in cat:
        video_actual = VIDEOS["maquinaria"]
    else:
        video_actual = VIDEOS["bienvenida"]
        
    texto_actual = model.generate_content(f"Saluda y presenta brevemente el tema: {user_input}").text

# 3. Renderizado directo
col1, col2 = st.columns(2)
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_actual)
with col2:
    st.subheader("Introducción")
    st.write(texto_actual)
