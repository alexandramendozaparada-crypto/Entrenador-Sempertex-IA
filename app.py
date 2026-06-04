import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs

# Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", page_icon="🏭")

# Configuración de APIs
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
eleven = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Cargar conocimiento
try:
    with open("manual.txt", "r", encoding="utf-8") as f:
        manual_contenido = f.read()
except:
    manual_contenido = "Información operativa de Sempertex."

# Configurar el modelo experto
# Asegúrate de que este bloque esté cerrado correctamente
system_prompt = f"Eres el entrenador experto de Sempertex. Responde a los empleados basándote en este manual: {manual_contenido}. Usa un tono profesional, técnico y empático."

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_prompt
)

st.title("🏭 Entrenador IA - Sempertex")
st.write("Tu asistente experto 24/7.")

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

if user_input:
    with st.spinner('Consultando expertos...'):
        # 1. Generar respuesta con Gemini
        response = model.generate_content(user_input)
        respuesta = response.text
        
        st.write(f"**Entrenador:** {respuesta}")
        
        # 2. Generar voz humana con ElevenLabs
        with st.spinner('Generando voz humana...'):
            audio_generator = eleven.generate(
                text=respuesta,
                voice="Bella",
                model="eleven_multilingual_v2"
            )
            
            # Guardar el audio generado
            with open("respuesta.mp3", "wb") as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            # 3. Reproducir audio
            st.audio("respuesta.mp3", format="audio/mp3", autoplay=True)
