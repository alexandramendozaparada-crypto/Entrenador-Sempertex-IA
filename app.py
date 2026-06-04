import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# 1. Configuración
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="Eres el presentador experto de Sempertex. Responde con un saludo breve."
)

videos = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# 2. Captura de Voz
st.write("---")
st.subheader("🎤 Pregunta por voz")
audio_data = mic_recorder(start_prompt="Presiona para hablar", stop_prompt="Detener", just_once=True)

# 3. Lógica para obtener el texto (ya sea por voz o por chat)
user_input = st.text_input("O escribe tu consulta aquí:")

final_query = user_input
if audio_data:
    # Nota: Aquí deberías integrar una API de transcripción (como Whisper).
    # Para la demo de mañana, lo más rápido es que el usuario use el texto.
    st.info("Audio capturado. (Integración de Whisper necesaria para procesar el audio).")

# 4. Procesamiento
col1, col2 = st.columns(2)
placeholder_video = col1.empty()

if final_query:
    with st.spinner('Procesando...'):
        prompt_cat = f"Clasifica '{final_query}' en 'sap', 'maquinaria' o 'bienvenida'. Solo una palabra."
        categoria = model.generate_content(prompt_cat).text.strip().lower()
        respuesta = model.generate_content(f"Saluda brevemente sobre: {final_query}").text
        
        # Mostrar Video
        with placeholder_video.container():
            st.subheader("Mentor Virtual")
            st.video(videos.get(categoria, videos["bienvenida"]))
        
        # Mostrar Texto
        with col2:
            st.subheader("Introducción")
            st.write(respuesta)
