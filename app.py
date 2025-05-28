import streamlit as st
import tempfile
import os
from src.audio_processor import AudioProcessor
from src.accent_classifier import EnglishAccentClassifier

st.title("English Accent Classifier")

st.write("Paste a YouTube/video/audio URL or upload an audio file (wav/mp3):")

url = st.text_input("Video or audio URL")
uploaded_file = st.file_uploader("Or upload an audio file", type=["wav", "mp3", "m4a", "webm"])

if st.button("Analyze"):
    try:
        processor = AudioProcessor()
        if url:
            st.info("Downloading and extracting audio from URL...")
            audio_path = processor.download_and_extract_audio(url)
        elif uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.read())
                tmp.flush()
                audio_path = processor._process_audio(tmp.name)
        else:
            st.warning("Please provide a URL or upload a file.")
            st.stop()

        st.success("Audio ready. Classifying accent...")
        classifier = EnglishAccentClassifier()
        results = classifier.classify_accent(audio_path)

        st.subheader("Results")
        st.write(f"**Language confidence:** {results['english_confidence']*100:.1f}%")
        st.write(f"**Accent:** {results['accent_classification']}")
        st.write(f"**Accent confidence:** {results['confidence_score']*100:.1f}%")
        st.write(f"**Explanation:** {results['explanation']}")
        st.write("**Transcription:**")
        st.write(results["transcription"])

    except Exception as e:
        st.error(f"Error: {str(e)}")