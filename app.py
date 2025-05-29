import streamlit as st
import tempfile
import os
import time

# Configuración de la página
st.set_page_config(
  page_title="English Accent Classifier",
  page_icon=None,
  layout="centered"
)

# Cache para los modelos pesados
@st.cache_resource
def load_audio_processor():
  """Carga el procesador de audio una sola vez"""
  from src.audio_processor import AudioProcessor
  return AudioProcessor()

@st.cache_resource
def load_accent_classifier():
  """Carga el clasificador una sola vez"""
  from src.accent_classifier import EnglishAccentClassifier
  return EnglishAccentClassifier()

def main():
  st.title("English Accent Classifier")
  st.markdown("---")

  # Mostrar estado de carga de modelos
  with st.status("Loading AI models...", expanded=True) as status:
    st.write("Loading audio processor...")
    processor = load_audio_processor()
    st.write("Audio processor ready")
    
    st.write("Loading accent classifier...")
    classifier = load_accent_classifier()
    st.write("Accent classifier ready")
    
    status.update(label="All models loaded!", state="complete", expanded=False)

  st.write("Upload an audio file or paste a video/audio URL to analyze the English accent:")

  # Crear tabs para mejor organización
  tab1, tab2 = st.tabs(["Upload File", "From URL"])

  with tab1:
    uploaded_file = st.file_uploader(
      "Choose an audio file", 
      type=["wav", "mp3", "m4a", "webm"],
      help="Supported formats: WAV, MP3, M4A, WEBM (Max 200MB)"
    )

  with tab2:
    url = st.text_input(
      "Video or audio URL", 
      placeholder="https://youtube.com/watch?v=...",
      help="Supports YouTube, Vimeo, and direct audio links"
    )

  # Botón de análisis
  if st.button("Analyze Accent", type="primary", disabled=False):
    if not url and not uploaded_file:
      st.warning("Please provide a URL or upload a file.")
      return
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
      # Procesar input
      if url:
        status_text.text("Downloading audio from URL...")
        progress_bar.progress(10)
        
        audio_path = processor.download_and_extract_audio(url)
        progress_bar.progress(40)
        status_text.text("Audio downloaded successfully!")
        
      elif uploaded_file:
        status_text.text("Processing uploaded file...")
        progress_bar.progress(10)
        
        # Verificar tamaño del archivo
        if uploaded_file.size > 200*1024*1024:  # 200MB
          st.error("File too large. Please upload files smaller than 200MB.")
          return
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
          tmp.write(uploaded_file.read())
          tmp.flush()
          audio_path = processor._process_audio(tmp.name)
        
        progress_bar.progress(40)
        status_text.text("File processed successfully!")

      # Clasificar acento
      status_text.text("Analyzing accent... This may take 30-60 seconds...")
      progress_bar.progress(60)
      
      start_time = time.time()
      results = classifier.classify_accent(audio_path)
      end_time = time.time()
      
      progress_bar.progress(100)
      status_text.text(f"Analysis completed in {end_time - start_time:.1f} seconds!")

      # Limpiar progress bar después de un momento
      time.sleep(1)
      progress_bar.empty()
      status_text.empty()

      # Mostrar resultados
      st.markdown("---")
      st.subheader("Analysis Results")
      
      # Crear columnas para mejor visualización
      col1, col2 = st.columns(2)
      
      with col1:
        st.metric(
          label="Language Confidence", 
          value=f"{results['english_confidence']*100:.1f}%",
          delta=None
        )
        
      with col2:
        st.metric(
          label="Accent Confidence", 
          value=f"{results['confidence_score']*100:.1f}%",
          delta=None
        )
      
      # Accent classification con destacado
      st.markdown(f"#### Detected Accent: **{results['accent_classification']}**")
      
      # Explicación
      st.markdown("#### Explanation")
      st.info(results['explanation'])
      
      # Transcripción
      if results.get("transcription"):
        st.markdown("#### Transcription")
        st.text_area(
          "Text content:", 
          results["transcription"], 
          height=150,
          disabled=True
        )

    except Exception as e:
      progress_bar.empty()
      status_text.empty()
      st.error(f"Error: {str(e)}")
      st.error("Please check your input and try again.")
      
      # Información de debug
      with st.expander("Debug Information"):
        st.code(str(e))

  # Información adicional
  with st.expander("How it works"):
    st.markdown("""
    This application analyzes English accents using machine learning:
    
    1. **Audio Processing**: Extracts and processes audio from your input
    2. **Language Detection**: Confirms the audio contains English speech
    3. **Accent Classification**: Identifies the specific English accent variant
    4. **Confidence Scoring**: Provides reliability metrics for the analysis
    
    **Supported Sources:**
    - Direct audio uploads (WAV, MP3, M4A, WEBM) - Max 200MB
    - YouTube videos
    - Vimeo videos
    - Direct audio URLs
    
    **Performance Tips:**
    - First analysis takes longer due to model loading
    - Subsequent analyses are faster (models cached)
    - Shorter audio clips process faster
    """)

  # Información de rendimiento
  with st.expander("Performance Info"):
    st.markdown("""
    **Expected Processing Times:**
    - Model loading: 30-60 seconds (first time only)
    - Audio download: 5-30 seconds
    - Accent analysis: 15-45 seconds
    
    **Tips for faster processing:**
    - Use shorter audio clips (1-3 minutes)
    - Prefer direct uploads over URLs when possible
    - Clear audio with minimal background noise works best
    """)

  # Footer
  st.markdown("---")
  st.markdown("Made with ❤️ using Streamlit | Optimized for Streamlit Cloud")

if __name__ == "__main__":
  main()