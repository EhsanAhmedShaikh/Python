# pip install streamlit
# pip install SpeechRecognition
# pip install requests
# pip install gTTS




import streamlit as st
import speech_recognition as sr
import requests
from gtts import gTTS
import tempfile
import os

# Define the language options
languages = ["English", "Urdu", "Arabic", "Chinese", "Spanish", "French"]





st.markdown("<h1 style='color: black;'>Get Yourself Translated</h1>", unsafe_allow_html=True)

st.subheader("Quick and Quality Voice Translation Service")


# Language Selection
source_language = st.selectbox("Select Source Language:", languages)
target_language = st.selectbox("Select Target Language:", languages)

# Language Codes
language_codes = {
    "English": "en",
    "Urdu": "ur",
    "Arabic": "ar",
    "Chinese": "zh",
    "Spanish": "es",
    "French": "fr"
}
# Create a Streamlit button
if st.button("Start Recording"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as mic:
        st.write("Recording... Speak now!")

        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

    try:
        text = recognizer.recognize_google(audio, language=language_codes[source_language])  # Recognize selected source language
        text = text.lower()
        st.write(f"Recognized Text ({source_language}):", text)

        # Translation API

        url = "https://text-translator2.p.rapidapi.com/translate"

        payload = {
            "source_language": language_codes[source_language],  # Use selected source language code
            "target_language": language_codes[target_language],  # Use selected target language code
            "text": text
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "3651494a1cmsh2ad6cebcd2dd2b8p173f91jsn5081c6ebd81a",
            "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }

        response = requests.post(url, headers=headers, data=payload)

        data = response.json()
        if "data" in data and "translatedText" in data["data"]:
            translated_text = data["data"]["translatedText"]
            st.write(f"Translated Text ({target_language}):", translated_text)

            # Text to Speech

            language = language_codes[target_language]  # Use selected target language code

            speech = gTTS(text=translated_text, lang=language, slow=False)
            
            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                tmpfile_name = tmpfile.name
                speech.save(tmpfile_name)
            
            # Display the audio in Streamlit
            st.audio(tmpfile_name, format="audio/mp3")

        else:
            st.write("Error:", data)

    except sr.UnknownValueError:
        st.write("Could not understand the audio.")
    except sr.RequestError as e:
        st.write(f"Error: {e}")

# Clean up temporary audio file when the Streamlit app exits
if 'tmpfile_name' in locals():
    os.remove(tmpfile_name)
