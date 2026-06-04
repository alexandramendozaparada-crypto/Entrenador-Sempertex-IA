import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")

# CSS para contraste extremo
st.markdown("""
    <style>
    /* Fondo limpio */
    .stApp {
        background-color: #ffffff; 
    }
    /* Todos los textos obligatoriamente en gris oscuro casi negro */
    div, p, h1, h2, h3, label, span {
        color: #262730 !important;
    }
    /* Títulos destacados en el color corporativo */
    h1, h2, h3 {
        color: #845ec2 !important;
    }
    /* Estilo del input */
    .stTextInput > div > div > input {
        border: 2px solid #845ec2 !important;
        background-color: #f9f9f9 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name='gemini-2.5-flash')
system_instruction="""
    Eres el entrenador IA de Sempertex. 
    1. Tus respuestas deben ser siempre profesionales, concisas y orientadas, debes ser entusiasta y amable.
    2. Si el tema no está relacionado con procedimientos internos de Sempertex o SAP, declina amablemente y redirige al usuario.
    3. Siempre utiliza un tono alentador pero corporativo.
    4. Limita tus respuestas a un máximo de 3 párrafos cortos.
    5. Centrate solo en la informacion que encuestras en manual.txt
    """


VIDEOS = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "mm": "introduccion-a-sap-modulo-mm-1080p-caption.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

st.title("Entrenador IA - Sempertex")

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

input_lower = user_input.lower()
video_actual = VIDEOS["bienvenida"]
texto_actual = "¡Bienvenido! ¿Cómo puedo ayudarte hoy con los procesos de Sempertex?"

if user_input:
    if 'mm' in input_lower:
        video_actual = VIDEOS["mm"]
        tema_ia = "el módulo SAP MM"
    elif 'sap' in input_lower:
        video_actual = VIDEOS["sap"]
        tema_ia = "SAP"
    else:
        video_actual = VIDEOS["bienvenida"]
        tema_ia = user_input
    
    texto_actual = model.generate_content(f"Saluda y presenta brevemente el tema: {tema_ia}").text

col1, col2 = st.columns(2)
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_actual)
with col2:
    st.subheader("Introducción Técnica")
    st.write(texto_actual)
