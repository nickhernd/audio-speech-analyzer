import streamlit as st
import tempfile
import os
from src.audio_processor import AudioProcessor
from src.accent_classifier import EnglishAccentClassifier

# Configuración de la página
st.set_page_config(
  page_title="English Accent Classifier",
  page_icon=None,
  layout="centered"
)

st.title("English Accent Classifier")
st.markdown("---")

st.write("Upload an audio file or paste a video/audio URL to analyze the English accent:")

# Crear tabs para mejor organización
tab1, tab2 = st.tabs(["Upload File", "From URL"])

with tab1:
  uploaded_file = st.file_uploader(
    "Choose an audio file", 
    type=["wav", "mp3", "m4a", "webm"],
    help="Supported formats: WAV, MP3, M4A, WEBM"
  )

with tab2:
  url = st.text_input(
    "Video or audio URL", 
    placeholder="https://youtube.com/watch?v=...",
    help="Supports YouTube, Vimeo, and direct audio links"
  )

# Botón de análisis
if st.button("Analyze Accent", type="primary"):
  if not url and not uploaded_file:
    st.warning("Please provide a URL or upload a file.")
    st.stop()
  
  try:
    # Inicializar procesador
    processor = AudioProcessor()
    
    # Procesar input
    if url:
      with st.spinner("Downloading and extracting audio from URL..."):
        audio_path = processor.download_and_extract_audio(url)
        st.success("Audio downloaded successfully!")
        
    elif uploaded_file:
      with st.spinner("Processing uploaded file..."):
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
          tmp.write(uploaded_file.read())
          tmp.flush()
          audio_path = processor._process_audio(tmp.name)
        st.success("File processed successfully!")

    # Clasificar acento
    with st.spinner("Analyzing accent... This may take a moment..."):
      classifier = EnglishAccentClassifier()
      results = classifier.classify_accent(audio_path)

    # Mostrar resultados
    st.markdown("---")
    st.subheader("Analysis Results")
    
    # Crear columnas para mejor visualización
    col1, col2 = st.columns(2)
    
    with col1:
      st.metric(
        label="Language Confidence", 
        value=f"{results['english_confidence']*100:.1f}%"
      )
      
    with col2:
      st.metric(
        label="Accent Confidence", 
        value=f"{results['confidence_score']*100:.1f}%"
      )
    
    # Accent classification con destacado
    st.markdown(f"### Detected Accent: **{results['accent_classification']}**")
    
    # Explicación
    st.markdown("### Explanation")
    st.info(results['explanation'])
    
    # Transcripción
    if results.get("transcription"):
      st.markdown("### Transcription")
      st.text_area(
        "Text content:", 
        results["transcription"], 
        height=150,
        disabled=True
      )

  except Exception as e:
    st.error(f"Error: {str(e)}")
    st.error("Please check your input and try again.")

# Información adicional
with st.expander("How it works"):
  st.markdown("""
  This application analyzes English accents using machine learning:
  
  1. **Audio Processing**: Extracts and processes audio from your input
  2. **Language Detection**: Confirms the audio contains English speech
  3. **Accent Classification**: Identifies the specific English accent variant
  4. **Confidence Scoring**: Provides reliability metrics for the analysis
  
  **Supported Sources:**
  - Direct audio uploads (WAV, MP3, M4A, WEBM)
  - YouTube videos
  - Vimeo videos
  - Direct audio URLs
  """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")