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
    "maquinaria": "modulomm.mp4", # Asegúrate de haber subido este archivo
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")
user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

if user_input:
    with st.spinner('Consultando expertos...'):
        # A. Clasificación de categoría
        prompt_cat = f"Responde solo con una palabra (sap, maquinaria, o bienvenida) basada en esta pregunta: {user_input}"
        categoria = model.generate_content(prompt_cat).text.strip().lower()
        
        # B. Generación de respuesta técnica
        respuesta = model.generate_content(user_input).text
        
        # C. Pantalla dividida
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Mentor Virtual")
            # Selección segura del video
            video_file = videos.get(categoria, videos["bienvenida"])
            try:
                st.video(video_path=video_file)
            except:
                st.warning("Video no disponible para esta consulta.")
        
        with col2:
            st.subheader("Respuesta Técnica")
            st.write(respuesta)
            
            # D. Voz nativa (Estable y sin errores de API)
            texto_voz = respuesta.replace('"', '').replace('\n', ' ')
            js_code = f"""
            <script>
                var msg = new SpeechSynthesisUtterance("{texto_voz}");
                msg.lang = 'es-ES';
                window.speechSynthesis.speak(msg);
            </script>
            """
            st.components.v1.html(js_code, height=0)
