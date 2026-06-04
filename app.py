import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from streamlit_audio_recorder import st_audio_recorder

# Configuración
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🤖 Entrenador IA - Sempertex (Voz)")

# 1. Grabación de voz del empleado
st.write("Presiona el botón y pregunta sobre procedimientos de Sempertex:")
audio_bytes = st_audio_recorder()

if audio_bytes:
    st.audio(audio_bytes, format='audio/wav')
    
    # Aquí iría un paso de transcripción (Whisper)
    # Para el MVP, simularemos que la transcripción es "Cómo es el proceso de seguridad"
    user_text = "Explícame el procedimiento de seguridad en línea 3" 
    st.write(f"**Empleado:** {user_text}")

    # 2. Generación de respuesta con Gemini
    with st.spinner('El entrenador está pensando...'):
        response = model.generate_content(f"Eres el experto de Sempertex. Responde: {user_text}")
        answer = response.text
        st.write(f"**Entrenador:** {answer}")

    # 3. Conversión de texto a voz (TTS)
    tts = gTTS(text=answer, lang='es')
    tts.save("respuesta.mp3")
    
    # 4. Reproducción
    st.audio("respuesta.mp3", format='audio/mp3', autoplay=True)

# Sección de Video (Placeholder para HeyGen)
st.divider()
st.subheader("Visualización del Avatar")
st.info("La integración de video con HeyGen API se activará en la Fase 2 mediante un endpoint de renderizado.")
