import os
from pathlib import Path
import yt_dlp
import librosa
import soundfile as sf
from config.settings import *

class AudioProcessor:
    def __init__(self):
        self.temp_dir = TEMP_DIR
        self.sample_rate = SAMPLE_RATE

    def download_and_extract_audio(self, url):
        """Download video and extract audio"""

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.temp_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'max_filesize': MAX_DOWNLOAD_SIZE,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'audio')

                audio_file = f"{self.temp_dir}/{title}.wav"

                if os.path.exists(audio_file):
                    return self._process_audio(audio_file)
                else:
                    raise FileNotFoundError("Could not extract audio")

        except Exception as e:
            raise Exception(f"Error downloading video: {str(e)}")

    def _process_audio(self, audio_path):
        """Process and normalize audio"""

        y, sr = librosa.load(audio_path, sr=self.sample_rate)

        if len(y) > MAX_AUDIO_LENGTH * self.sample_rate:
            y = y[:MAX_AUDIO_LENGTH * self.sample_rate]

        y = librosa.util.normalize(y)

        output_path = PROCESSED_AUDIO_DIR / f"processed_{Path(audio_path).stem}.wav"
        sf.write(output_path, y, self.sample_rate)

        return str(output_path)
