import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# 1. Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", page_icon="🏭")

# 2. Configuración de APIs (Usa los Secrets de Streamlit)
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

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=system_prompt
)

# 5. Interfaz de Usuario
st.title("🏭 Entrenador IA - Sempertex")
st.write("Tu asistente experto 24/7 para procedimientos y seguridad.")

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

if user_input:
    with st.spinner('Consultando expertos...'):
        # A. Generar respuesta con Gemini
        response = model.generate_content(user_input)
        respuesta = response.text
        
        st.write(f"**Entrenador:** {respuesta}")
        
        # B. Generar voz humana con ElevenLabs (Sintaxis actualizada 1.x+)
        with st.spinner('Generando voz humana...'):
            try:
                audio_generator = client.generate(
                    text=respuesta,
                    voice="b2htR0pMe28pYwCY9gnP",
                    model="eleven_multilingual_v2"
                )
                
                # Guardar el audio generado
                with open("respuesta.mp3", "wb") as f:
                    for chunk in audio_generator:
                        f.write(chunk)
                
                # C. Reproducir audio
                st.audio("respuesta.mp3", format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Error al generar la voz: {e}")
