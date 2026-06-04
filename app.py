import streamlit as st
import google.generativeai as genai
import os

# Configuración (Usa los Secrets de Streamlit para no subir tu API KEY a GitHub)
genai.configure(api_key=st.secrets["AQ.Ab8RN6JYhwUnH5le9on4OwEGbg1-iyINSb2xMXuRS-xAZYXIxA"])

st.set_page_config(page_title="Entrenador IA Sempertex", page_icon="🤖")

st.title("🤖 Entrenador IA - Sempertex")

# Carga de contexto (puedes tener un archivo 'manual.txt' en tu repo)
with open("manual.txt", "r", encoding="utf-8") as f:
    contexto = f.read()

model = genai.GenerativeModel('gemini-1.5-flash')

user_input = st.text_input("¿En qué puedo ayudarte hoy?")

if user_input:
    with st.spinner('Consultando los manuales...'):
        prompt = f"Actúa como un experto en Sempertex. Usa esta información para responder: {contexto}\n\nPregunta: {user_input}"
        response = model.generate_content(prompt)
        st.write(response.text)
