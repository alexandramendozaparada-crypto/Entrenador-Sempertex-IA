import streamlit as st
import google.generativeai as genai

# 1. Configuración
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name='gemini-2.5-flash')

# 2. Archivos (Asegúrate de que estos nombres sean exactos en tu repo)
VIDEOS = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "maquinaria": "modulomm.mp4", # <--- Este es el de MM
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("🏭 Entrenador IA - Sempertex")

# Inicializar sesión
if 'video_path' not in st.session_state:
    st.session_state.video_path = VIDEOS["bienvenida"]
    st.session_state.texto = "¡Hola! ¿Cómo puedo ayudarte hoy?"

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

if user_input:
    with st.spinner('Actualizando mentor...'):
        # Clasificación mucho más inteligente
        prompt = f"De estas opciones: 'sap', 'maquinaria' (que incluye MM), 'bienvenida'. ¿A qué categoría pertenece la consulta: '{user_input}'? Responde SOLO la palabra."
        cat = model.generate_content(prompt).text.strip().lower()
        
        # Asignar video basado en la palabra clave
        if 'sap' in cat:
            st.session_state.video_path = VIDEOS["sap"]
        elif 'maquinaria' in cat or 'mm' in cat:
            st.session_state.video_path = VIDEOS["maquinaria"]
        else:
            st.session_state.video_path = VIDEOS["bienvenida"]
            
        # Respuesta corta (sin explicaciones técnicas largas si ya tenemos video)
        st.session_state.texto = model.generate_content(f"Saluda al operario y presenta brevemente el tema: {user_input}").text
        
        st.rerun() # Fuerza a que la interfaz muestre el nuevo video inmediatamente

# Renderizado
col1, col2 = st.columns(2)
with col1:
    st.subheader("Mentor Virtual")
    st.video(st.session_state.video_path)

with col2:
    st.subheader("Introducción")
    st.write(st.session_state.texto)
