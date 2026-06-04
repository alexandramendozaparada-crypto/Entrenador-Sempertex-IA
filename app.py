import streamlit as st
import google.generativeai as genai

# 1. Configuración
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction="Eres el presentador experto de Sempertex. Responde con un saludo breve."
)

videos = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# Inicializamos el estado del video si no existe
if 'categoria' not in st.session_state:
    st.session_state.categoria = "bienvenida"
    st.session_state.respuesta = "¡Bienvenido! ¿Cómo puedo ayudarte hoy?"

# 2. Entrada del usuario
user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# 3. Lógica: Solo actualizamos si el usuario escribe algo nuevo
if user_input:
    with st.spinner('Procesando...'):
        prompt_cat = f"Clasifica '{user_input}' en 'sap', 'maquinaria' o 'bienvenida'. Solo una palabra."
        st.session_state.categoria = model.generate_content(prompt_cat).text.strip().lower()
        st.session_state.respuesta = model.generate_content(f"Saluda brevemente sobre: {user_input}").text

# 4. Renderizado
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mentor Virtual")
    # El video siempre toma el valor actual del estado
    video_path = videos.get(st.session_state.categoria, videos["bienvenida"])
    st.video(video_path)

with col2:
    st.subheader("Introducción")
    st.write(st.session_state.respuesta)
