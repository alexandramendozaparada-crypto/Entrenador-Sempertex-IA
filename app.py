import streamlit as st
import google.generativeai as genai

# 1. Configuración de página
st.set_page_config(page_title="Entrenador IA Sempertex", layout="wide")

# 2. Diseño CSS Profesional
st.markdown(f"""
    <style>
    /* Fondo general */
    .stApp {{
        background-color: #f4f4f9;
    }}
    /* Títulos con el color corporativo */
    h1, h2, h3 {{
        color: #845ec2 !important;
        font-family: sans-serif;
    }}
    /* Corregir color de texto en columnas para que sea legible */
    .stMarkdown, .stText {{
        color: #333333 !important;
    }}
    /* Caja de entrada estilizada */
    .stTextInput > div > div > input {{
        border: 2px solid #845ec2;
        border-radius: 8px;
        background-color: white;
    }}
    /* Borde del video */
    [data-testid="stVideo"] {{
        border: 4px solid #845ec2;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. Configuración de API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name='gemini-2.5-flash')

# 4. Nombres exactos de archivos
VIDEOS = {
    "sap": "Introducción a SAP_ El ERP Líder_1080p.mp4",
    "mm": "introduccion-a-sap-modulo-mm-1080p-caption.mp4",
    "bienvenida": "Bienvenida Sempertex - Asistente IA_1080p_caption.mp4"
}

# Título con logo de texto
st.title("🏭 Entrenador IA - Sempertex")

user_input = st.text_input("¿Qué procedimiento necesitas consultar?")

# 5. Lógica funcional (La que ya probamos que funciona)
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

# 6. Renderizado limpio
col1, col2 = st.columns(2)
with col1:
    st.subheader("Mentor Virtual")
    st.video(video_actual)
with col2:
    st.subheader("Introducción Técnica")
    st.write(texto_actual)
