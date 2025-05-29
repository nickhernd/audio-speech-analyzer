from flask import Flask, request, jsonify
import traceback

from src.audio_processor import AudioProcessor
from src.accent_classifier import EnglishAccentClassifier

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        processor = AudioProcessor()
        audio_path = processor.download_and_extract_audio(url)
        classifier = EnglishAccentClassifier()
        results = classifier.classify_accent(audio_path)
        return jsonify(results)
    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()  # Esto imprime el error completo en los logs
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return '''
    <html>
    <head>
      <title>English Accent Classifier API</title>
      <style>
        body { font-family: Arial, sans-serif; background: #f4f6fb; color: #222; }
        .container { max-width: 500px; margin: 60px auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 32px; }
        h2 { text-align: center; color: #2a4d7a; }
        label { font-weight: bold; }
        input[type="text"] { width: 100%; padding: 10px; margin: 12px 0 20px 0; border: 1px solid #ccc; border-radius: 6px; }
        button { background: #2a4d7a; color: #fff; border: none; padding: 10px 24px; border-radius: 6px; cursor: pointer; font-size: 1em; }
        button:hover { background: #183153; }
        #result { margin-top: 24px; padding: 16px; background: #f0f8ff; border-radius: 8px; min-height: 32px; }
        .error { color: #c00; }
      </style>
    </head>
    <body>
      <div class="container">
        <h2>English Accent Classifier</h2>
        <form id="analyzeForm">
          <label for="url">Video/Audio URL:</label>
          <input name="url" id="url" type="text" placeholder="https://..." required>
          <button type="submit">Analyze</button>
        </form>
        <div id="result"></div>
        <p style="font-size:0.95em;color:#888;margin-top:32px;">
          Send a POST request to <code>/analyze</code> with JSON: {"url": "https://..."}</p>
      </div>
      <script>
        document.getElementById('analyzeForm').onsubmit = async function(e) {
          e.preventDefault();
          const url = document.getElementById('url').value;
          const resultDiv = document.getElementById('result');
          resultDiv.innerHTML = "Analyzing...";
          try {
            const response = await fetch('/analyze', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({url})
            });
            const data = await response.json();
            if (response.ok) {
              resultDiv.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } else {
              resultDiv.innerHTML = '<span class="error">' + (data.error || 'Unknown error') + '</span>';
            }
          } catch (err) {
            resultDiv.innerHTML = '<span class="error">Request failed</span>';
          }
        }
      </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

import streamlit as st
import tempfile
import os
from src.audio_processor import AudioProcessor
from src.accent_classifier import EnglishAccentClassifier

st.title("English Accent Classifier")

st.write("Paste a video/audio URL or upload an audio file (mp3, wav):")

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
        st.write(results.get("transcription", ""))

    except Exception as e:
        st.error(f"Error: {str(e)}")