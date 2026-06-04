import streamlit as st
import google.generativeai as genai

# 1. Configuración
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# INSTRUCCIÓN CLAVE: Le decimos que su respuesta debe ser corta y directa para acompañar el video
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="""Eres el presentador experto de Sempertex. 
    Tu objetivo es introducir el video que se está mostrando. 
    Responde siempre con una frase corta, profesional y entusiasta (máximo 2 líneas). 
    No des explicaciones técnicas largas, deja que el video lo haga."""
)

videos = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")
col1, col2 = st.columns(2)
user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# 2. Lógica de selección
video_file = videos["bienvenida"]
respuesta = "¡Hola! Soy tu asistente de Sempertex. Selecciona un tema para comenzar."

if user_input:
    with st.spinner('Cargando módulo...'):
        # Clasificar para saber qué video poner
        prompt_cat = f"Clasifica la pregunta en 'sap', 'maquinaria' o 'bienvenida'. Responde solo la palabra: {user_input}"
        categoria = model.generate_content(prompt_cat).text.strip().lower()
        
        # Generar una frase corta introductoria
        respuesta = model.generate_content(f"Presenta brevemente este tema para un video: {user_input}").text
        
        # Asignar video
        video_file = videos.get(categoria, videos["bienvenida"])

# 3. Visualización
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_file)

with col2:
    st.subheader("Introducción")
    st.write(respuesta)
    
    # Voz solo para la frase introductoria corta
    texto_voz = respuesta.replace('"', '').replace('\n', ' ')
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{texto_voz}");
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)
