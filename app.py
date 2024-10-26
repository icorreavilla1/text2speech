import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Título y subtítulo principal
st.title("🦊 Conversión de Texto a Audio")
st.subheader("Conviértete en el narrador de una fábula mágica 🌙")

# Imagen destacada de la aplicación
image = Image.open('fabula.png')  # Asegúrate de tener una imagen de fábula atractiva
st.image(image, use_column_width=True)

# Configuración de la barra lateral
with st.sidebar:
    st.subheader("💬 Introduce o selecciona el texto para escuchar")
    st.write("Selecciona el idioma y escucha la historia en audio.")

# Crear la carpeta temporal para los archivos de audio
if not os.path.exists("temp"):
    os.mkdir("temp")

# Nueva fábula para mostrar
st.subheader("🌌 Una Fábula de la Luna y la Noche 🌌")
st.write(
    "Había una vez una Luna que cada noche brillaba más intensamente. Los animales nocturnos, maravillados, "
    "se reunían para admirarla. Pero, un día, la Noche le dijo: "
    "'Querida Luna, ¿por qué brillas tan fuerte?'. "
    "La Luna respondió: 'Porque quiero guiar a quienes buscan en la oscuridad'. "
    "Y desde entonces, la Luna ilumina, y los animales siguen su luz en silencio. "
)

st.markdown("### ¿Te gustaría escuchar esta historia? Copia el texto o introduce el tuyo propio. ✨")
text = st.text_area("Introduce el texto aquí:")

# Selección de idioma
option_lang = st.selectbox("🌍 Selecciona el idioma", ["Español", "English"])
language_code = 'es' if option_lang == "Español" else 'en'

# Función de conversión de texto a voz
def text_to_speech(text, language_code):
    tts = gTTS(text, lang=language_code)
    file_name = text[:15] if len(text) > 15 else "audio"
    tts.save(f"temp/{file_name}.mp3")
    return file_name

# Botón para convertir a audio
if st.button("🎙️ Convertir a Audio"):
    file_name = text_to_speech(text, language_code)
    audio_path = f"temp/{file_name}.mp3"
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    
    st.markdown("### Tu audio 🎧:")
    st.audio(audio_bytes, format="audio/mp3")
    
    # Descargar archivo de audio
    def download_audio(bin_file, label="Descargar Audio"):
        with open(bin_file, "rb") as file:
            data = file.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{label}</a>'
            return href
    
    st.markdown(download_audio(audio_path), unsafe_allow_html=True)

# Limpieza de archivos temporales
def remove_files(days_old=7):
    now = time.time()
    for file in glob.glob("temp/*.mp3"):
        if os.stat(file).st_mtime < now - days_old * 86400:
            os.remove(file)

remove_files()

