import streamlit as st
import google.generativeai as genai

# 1. Configuración
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="Clasifica brevemente la pregunta para activar un video. Responde con un saludo corto."
)

videos = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# Creamos un contenedor vacío para que el video se actualice siempre
col1, col2 = st.columns(2)
placeholder_video = col1.empty() 

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# Lógica
categoria = "bienvenida"
respuesta = "¡Bienvenido! ¿Cómo puedo ayudarte hoy?"

if user_input:
    with st.spinner('Activando video...'):
        prompt_cat = f"Clasifica la pregunta en 'sap', 'maquinaria' o 'bienvenida'. Solo una palabra: {user_input}"
        categoria = model.generate_content(prompt_cat).text.strip().lower()
        respuesta = model.generate_content(f"Saluda brevemente sobre: {user_input}").text

# 2. Renderizado (Forzamos la actualización)
with placeholder_video.container():
    st.subheader("Mentor Virtual")
    video_file = videos.get(categoria, videos["bienvenida"])
    st.video(video_file)

with col2:
    st.subheader("Introducción")
    st.write(respuesta)
    # Ya NO incluimos el código de voz, porque el video de HeyGen ya habla por sí solo.
