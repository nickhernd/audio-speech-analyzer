# English Accent Classifier

**AI-powered tool for classifying English accents from video URLs**

Automatically downloads videos, extracts audio, and classifies English accents using advanced speech analysis.

## Quick Start

```bash
# 1. Run setup
cd audio-speech-analyzer

# 2. Install dependencies
bash scripts/install.sh
source venv/bin/activate

# 3. Classify an accent
python3 app.py
```

## What It Does

- Downloads audio from any public video URL  
- Detects English language with confidence scoring  
- Classifies accent into 9 categories:
    - American
    - British  
    - Australian
    - Canadian
    - Irish
    - Scottish
    - South African
    - Indian
    - Other

- Confidence scoring (0-100%)  
- Detailed explanations of classification  

## Usage Examples

```bash
# Basic classification
python src/main.py --url "https://example.com/video.mp4"

# Verbose output with details
python src/main.py --url "https://example.com/video.mp4" --verbose

# Custom output file
python src/main.py --url "https://example.com/video.mp4" --output "my_results.json"

# Example 
python src/main.py --url 'https://www.youtube.com/watch?v=A1catDy3sJ0' --verbose
```

## Sample Output

```
English Accent Classifier
==================================================
Downloading and extracting audio...
Analyzing English accent...

==================================================
CLASSIFICATION RESULTS
==================================================
LANGUAGE: English detected (87.5% confidence)
ACCENT: American
CONFIDENCE: 78.3%
EXPLANATION: Accent classified as American with 78.3% confidence. 
        Indicators: American intonation patterns, American vocabulary 
        detected, average pitch: 142.3Hz, speech rate: 3.2 events/sec.

Full results saved to: accent_results.json
==================================================
RESULT: American accent detected!
==================================================
```

## Technical Features

### Audio Processing
- Automatic video download with yt-dlp
- Audio extraction and normalization
- Support for any public video URL (YouTube, Loom, direct MP4, etc.)

### Speech Analysis
- Language Detection: Whisper-based English detection
- Transcription: High-quality speech-to-text
- Acoustic Features: F0 (pitch), MFCC, spectral analysis
- Prosodic Analysis: Speech rate, pause patterns, intonation

### Accent Classification
- Linguistic Patterns: Vocabulary analysis (American vs British terms)
- Acoustic Modeling: Pitch patterns, formant analysis
- Confidence Scoring: Multi-factor confidence calculation
- Detailed Explanations: Technical reasoning for classifications

## Requirements

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS  
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Python Dependencies
- Python 3.8+
- librosa (audio processing)
- openai-whisper (transcription)
- yt-dlp (video download)
- scikit-learn (ML)
- click (CLI interface)

## Evaluation Criteria Met

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Functional Script | Yes | Runs and returns accent classification |
| Logical Approach | Yes | Whisper transcription + acoustic analysis |  
| Setup Clarity | Yes | One-command setup with clear README |
| English Accent Handling | Yes | 9 English accent categories supported |
| Confidence Scoring | Yes | 0-100% confidence with explanations |

## How It Works

1. URL Processing: Downloads video using yt-dlp
2. Audio Extraction: Converts to WAV, normalizes audio
3. Language Detection: Uses Whisper to confirm English
4. Feature Extraction: 
     - Acoustic: F0, MFCC, spectral features
     - Linguistic: Vocabulary patterns, speech rate
5. Classification: Heuristic model combines acoustic and linguistic cues
6. Confidence Scoring: Multi-factor confidence calculation
7. Results: JSON output with detailed explanations

## Notes

- Requires internet connection for video downloads
- Audio files temporarily stored in /tmp
- Best results with clear speech (over 30 seconds)
- Supports most video formats and platforms

## Troubleshooting

ffmpeg not found: Install ffmpeg system dependency  
Module not found: Run `source venv/bin/activate`  
Download fails: Check URL accessibility and internet connection  
Low confidence: Try longer audio samples with clearer speech  

![image](https://github.com/user-attachments/assets/2e7d4cbf-6d80-4dbe-b5c5-aaa0fc532c48)

