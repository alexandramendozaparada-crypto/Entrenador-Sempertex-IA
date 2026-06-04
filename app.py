import streamlit as st
import google.generativeai as genai

# Configuración
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🤖 Entrenador IA - Sempertex")

user_input = st.text_input("¿Qué necesitas saber sobre la operación?")

if user_input:
    response = model.generate_content(user_input)
    respuesta = response.text
    st.write(f"**Entrenador:** {respuesta}")
    
    # JavaScript para que el navegador hable (Voz estable)
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{respuesta.replace('"', '')}");
        msg.lang = 'es-ES';
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)
