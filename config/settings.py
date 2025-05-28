import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
PROCESSED_AUDIO_DIR = DATA_DIR / "processed_audio"
SAMPLE_VIDEOS_DIR = DATA_DIR / "sample_videos"

# Configuración de audio
SAMPLE_RATE = 16000
AUDIO_FORMAT = "wav"
MAX_AUDIO_LENGTH = 300  # 5 minutos máximo

# Configuración de modelos
WHISPER_MODEL = "base"
CONFIDENCE_THRESHOLD = 0.7

# URLs y APIs
TEMP_DIR = "/tmp"
MAX_DOWNLOAD_SIZE = 100 * 1024 * 1024  # 100MB

# Logging
LOG_LEVEL = "INFO"
