import streamlit as st
import google.generativeai as genai

# 1. Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")

# 2. Configuración de API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Diccionario de videos (nombres exactos según tu repo)
videos = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# Creamos las columnas fuera del if para que siempre existan
col1, col2 = st.columns(2)

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# Lógica para determinar qué mostrar
if user_input:
    with st.spinner('Consultando expertos...'):
        prompt_cat = f"Responde solo con una palabra (sap, maquinaria, o bienvenida) basada en esta pregunta: {user_input}"
        categoria = model.generate_content(prompt_cat).text.strip().lower()
        respuesta = model.generate_content(user_input).text
        
        video_file = videos.get(categoria, videos["bienvenida"])
else:
    # Estado inicial: bienvenida
    video_file = videos["bienvenida"]
    respuesta = "¡Hola! ¿Cómo puedo ayudarte hoy?"

# Mostrar contenido
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_file)

with col2:
    st.subheader("Respuesta Técnica")
    st.write(respuesta)
    
    # Voz nativa para la bienvenida o respuesta
    texto_voz = respuesta.replace('"', '').replace('\n', ' ')
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{texto_voz}");
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)
