import streamlit as st
import google.generativeai as genai

# 1. Configuración de API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Cargar el manual
try:
    with open("manual.txt", "r", encoding="utf-8") as f:
        manual_contenido = f.read()
except:
    manual_contenido = "Información general de Sempertex disponible."

# 3. Configurar el modelo con instrucciones de sistema
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=f"Eres el entrenador experto de Sempertex. Responde a los empleados basándote solo en este manual: {manual_contenido}. Si no sabes algo, sé honesto y pide que llamen a su supervisor."
)

# 4. Interfaz
st.title("🤖 Entrenador IA - Sempertex")
st.write("---")

user_input = st.text_input("¿Qué duda técnica tienes hoy?")

if user_input:
    with st.spinner('Consultando los manuales...'):
        response = model.generate_content(user_input)
        respuesta = response.text
        
        st.write(f"**Entrenador:** {respuesta}")
        
        # 5. Voz Nativa (Hablar respuesta)
        # Limpiamos el texto de caracteres especiales para que la voz no falle
        texto_limpio = respuesta.replace('"', '').replace('\n', ' ')
        js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{texto_limpio}");
            msg.lang = 'es-ES';
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_code, height=0)
