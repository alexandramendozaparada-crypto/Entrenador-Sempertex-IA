import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🏭 Entrenador IA - Sempertex")

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# Diccionario de videos pregrabados (asegúrate de que los nombres coincidan en la carpeta /videos)
videos = {
    "SAP": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "videos/modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

if user_input:
    # 1. Clasificamos la intención con Gemini
    prompt_clasificacion = f"Clasifica la siguiente pregunta en una de estas categorías: 'seguridad', 'maquinaria' o 'general'. Responde SOLO con la palabra. Pregunta: {user_input}"
    categoria = model.generate_content(prompt_clasificacion).text.strip().lower()
    
    # 2. Obtenemos la respuesta técnica de Gemini
    respuesta = model.generate_content(user_input).text
    
    # 3. Presentación en pantalla dividida
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mentor Virtual")
        # Reproduce el video según la categoría
        video_path = videos.get(categoria, videos["general"])
        st.video(video_path)
        
    with col2:
        st.subheader("Respuesta Técnica")
        st.write(respuesta)
        
        # Voz nativa para acompañar al video
        js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{respuesta.replace('"', '')}");
            msg.lang = 'es-ES';
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_code, height=0)
