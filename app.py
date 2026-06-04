import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import generate, save

# 1. Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", page_icon="🏭")

# 2. Configuración de APIs (Usando Secrets)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Inicializamos el cliente de ElevenLabs
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
    model_name='gemini-1.5-flash',
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
        
        # B. Generar voz humana con ElevenLabs
        with st.spinner('Generando voz humana...'):
            try:
                # Usamos la sintaxis estable de la versión 0.3.0
                audio = generate(
                    text=respuesta,
                    voice="sofia",
                    model="eleven_multilingual_v2",
                    api_key=st.secrets["ELEVENLABS_API_KEY"]
                )
                
                # Guardar el audio generado
                save(audio, "respuesta.mp3")
                
                # C. Reproducir audio
                st.audio("respuesta.mp3", format="audio/mp3", autoplay=True)
            except Exception as e:
                st.error(f"Error al generar la voz: {e}")
