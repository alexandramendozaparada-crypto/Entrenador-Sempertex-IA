import streamlit as st
import google.generativeai as genai

# 1. Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")

# 2. Configuración de API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="Eres un supervisor experto de Sempertex. Responde de forma profesional, técnica, segura y empática."
)

# 3. Diccionario de videos (nombres exactos según tu repo)
videos = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# Creamos columnas
col1, col2 = st.columns(2)

# Entrada del usuario
user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# 4. Lógica de selección de video y respuesta
video_file = videos["bienvenida"] # Default
respuesta = ""

if user_input:
    with st.spinner('Procesando consulta...'):
        # Clasificación
        prompt_cat = f"Clasifica la pregunta en 'sap', 'maquinaria' o 'bienvenida'. Responde solo una palabra: {user_input}"
        categoria = model.generate_content(prompt_cat).text.strip().lower()
        
        # Generar respuesta
        respuesta = model.generate_content(user_input).text
        
        # Seleccionar video
        video_file = videos.get(categoria, videos["bienvenida"])

# 5. Mostrar en pantalla
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_file)

with col2:
    st.subheader("Respuesta Técnica")
    if user_input:
        st.write(respuesta)
        # Voz nativa solo cuando hay respuesta
        texto_voz = respuesta.replace('"', '').replace('\n', ' ')
        js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{texto_voz}");
            msg.lang = 'es-ES';
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_code, height=0)
    else:
        st.info("Escribe una pregunta para obtener asistencia técnica sobre los procesos de Sempertex.")
