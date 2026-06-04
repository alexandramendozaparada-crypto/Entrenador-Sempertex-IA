import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# 1. Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", page_icon="🏭")

# 2. Configuración de APIs
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# 3. Cargar conocimiento
try:
    with open("manual.txt", "r", encoding="utf-8") as f:
        manual_contenido = f.read()
except:
    manual_contenido = "Información operativa de Sempertex."

# 4. Configurar el modelo experto
system_prompt = f"Eres el entrenador experto de Sempertex. Responde a los empleados basándote en este manual: {manual_contenido}. Usa un tono profesional, técnico y empático."
model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=system_prompt)

# 5. Interfaz
st.title("🏭 Entrenador IA - Sempertex")

# Campo para que el usuario elija la voz (funcionalidad extra)
voice_id = st.text_input("ID de la voz (o nombre):", value="Bella") 
user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

if user_input:
    with st.spinner('Consultando expertos...'):
        response = model.generate_content(user_input)
        respuesta = response.text
        st.write(f"**Entrenador:** {respuesta}")
        
        with st.spinner('Generando voz humana...'):
            try:
                # SINTAXIS CORRECTA PARA ELEVENLABS 1.X
                audio_generator = client.text_to_speech.convert(
                    text=respuesta,
                    voice_id=b2htR0pMe28pYwCY9gnP,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )
                
                # Guardar el audio (el generador de la versión 1.x devuelve un stream)
                with open("respuesta.mp3", "wb") as f:
                    for chunk in audio_generator:
                        f.write(chunk)
                
                st.audio("respuesta.mp3", format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Error en voz: {e}")
