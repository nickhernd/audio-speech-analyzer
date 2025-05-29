import streamlit as st
import tempfile
import os
import time
import sys
import traceback

# Configuración de la página
st.set_page_config(
  page_title="English Accent Classifier",
  page_icon=None,
  layout="centered"
)

# Estado global para evitar recargas
if 'models_loaded' not in st.session_state:
  st.session_state.models_loaded = False
  st.session_state.processor = None
  st.session_state.classifier = None

def load_models():
  """Carga los modelos de forma segura con manejo de errores"""
  try:
    if not st.session_state.models_loaded:
      # Mostrar el progreso de carga
      loading_placeholder = st.empty()
      
      with loading_placeholder.container():
        st.info("Initializing application... This may take 1-2 minutes on first load.")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Cargar AudioProcessor
        status_text.text("Loading audio processor...")
        progress_bar.progress(25)
        
        from src.audio_processor import AudioProcessor
        st.session_state.processor = AudioProcessor()
        
        status_text.text("Audio processor loaded")
        progress_bar.progress(50)
        
        # Cargar AccentClassifier
        status_text.text("Loading accent classifier...")
        progress_bar.progress(75)
        
        from src.accent_classifier import EnglishAccentClassifier
        st.session_state.classifier = EnglishAccentClassifier()
        
        status_text.text("All models loaded successfully!")
        progress_bar.progress(100)
        
        time.sleep(1)
        st.session_state.models_loaded = True
      
      # Limpiar el placeholder de carga
      loading_placeholder.empty()
      st.success("Application ready! You can now analyze audio.")
      st.rerun()
      
  except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    st.error("Debug info:")
    st.code(traceback.format_exc())
    
    # Botón para reintentar
    if st.button("Retry Loading Models"):
      st.session_state.models_loaded = False
      st.session_state.processor = None
      st.session_state.classifier = None
      st.rerun()
    
    st.stop()

def main():
  st.title("English Accent Classifier")
  st.markdown("---")
  
  # Cargar modelos si no están cargados
  if not st.session_state.models_loaded:
    load_models()
    return
  
  # Interface principal (solo se muestra cuando los modelos están listos)
  st.write("Upload an audio file or paste a video/audio URL to analyze the English accent:")

  # Crear tabs
  tab1, tab2 = st.tabs(["Upload File", "From URL"])

  url = None
  uploaded_file = None

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
  if st.button("Analyze Accent", type="primary"):
    if not url and not uploaded_file:
      st.warning("Please provide a URL or upload a file.")
      return
    
    analyze_audio(url, uploaded_file)

def analyze_audio(url, uploaded_file):
  """Función separada para analizar el audio"""
  
  # Progress tracking
  progress_bar = st.progress(0)
  status_text = st.empty()
  
  try:
    # Obtener los modelos del session state
    processor = st.session_state.processor
    classifier = st.session_state.classifier
    
    audio_path = None
    
    # Procesar input
    if url:
      status_text.text("Downloading audio from URL...")
      progress_bar.progress(20)
      
      audio_path = processor.download_and_extract_audio(url)
      status_text.text("Audio downloaded!")
      progress_bar.progress(40)
      
    elif uploaded_file:
      status_text.text("Processing uploaded file...")
      progress_bar.progress(20)
      
      # Verificar tamaño
      if uploaded_file.size > 200*1024*1024:  # 200MB
        st.error("File too large. Please upload files smaller than 200MB.")
        return
      
      # Crear archivo temporal
      with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp.flush()
        audio_path = processor._process_audio(tmp.name)
      
      status_text.text("File processed!")
      progress_bar.progress(40)

    # Clasificar acento
    status_text.text("Analyzing accent... Please wait...")
    progress_bar.progress(60)
    
    start_time = time.time()
    results = classifier.classify_accent(audio_path)
    end_time = time.time()
    
    progress_bar.progress(100)
    status_text.text(f"Analysis completed in {end_time - start_time:.1f} seconds!")

    # Limpiar indicadores
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()

    # Mostrar resultados
    display_results(results)

  except Exception as e:
    progress_bar.empty()
    status_text.empty()
    st.error(f"Error during analysis: {str(e)}")
    
    with st.expander("Debug Information"):
      st.code(traceback.format_exc())

def display_results(results):
  """Mostrar los resultados del análisis"""
  
  st.markdown("---")
  st.subheader("Analysis Results")
  
  # Métricas en columnas
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
  
  # Resultado principal
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

# Información y footer (siempre visible)
def show_footer():
  # Información adicional
  with st.expander("How it works"):
    st.markdown("""
    This application analyzes English accents using machine learning:
    
    1. Audio Processing: Extracts and processes audio from your input
    2. Language Detection: Confirms the audio contains English speech  
    3. Accent Classification: Identifies the specific English accent variant
    4. Confidence Scoring: Provides reliability metrics for the analysis
    
    Supported Sources:
    - Direct audio uploads (WAV, MP3, M4A, WEBM) - Max 200MB
    - YouTube videos, Vimeo videos, Direct audio URLs
    """)

  with st.expander("Performance Tips"):
    st.markdown("""
    Loading Times:
    - First load: 1-2 minutes (loading AI models)
    - Subsequent uses: Much faster (models cached)
    - Analysis: 15-60 seconds depending on audio length
    
    For Best Results:
    - Use clear audio with minimal background noise
    - 1-5 minute clips work best
    - English speech only
    """)

  # Footer
  st.markdown("---")
  st.markdown("Made with ❤️ using Streamlit | Optimized for Cloud Deployment")

# Ejecutar la aplicación
if __name__ == "__main__":
  main()
  show_footer()