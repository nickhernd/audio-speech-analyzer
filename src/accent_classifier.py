import librosa
import numpy as np
import whisper
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from config.settings import *

class EnglishAccentClassifier:
    def __init__(self):
        self.whisper_model = whisper.load_model(WHISPER_MODEL)
        self.accent_categories = [
            "American", "British", "Australian", "Canadian", 
            "Irish", "Scottish", "South African", "Indian", "Other"
        ]
        
    def classify_accent(self, audio_path):
        """Classifies the English accent in the audio"""
        
        results = {
            "accent_classification": None,
            "confidence_score": 0,
            "english_confidence": 0,
            "transcription": "",
            "explanation": ""
        }
        
        try:
            # 1. Transcription and language detection
            transcription_result = self._transcribe_with_language_detection(audio_path)
            results["transcription"] = transcription_result["text"]
            
            # 2. Check if it's English
            english_confidence = self._detect_english_confidence(transcription_result)
            results["english_confidence"] = english_confidence
            
            if english_confidence < 0.7:
                results["explanation"] = f"Audio detected as non-English (confidence: {english_confidence:.2f})"
                return results
            
            # 3. Extract acoustic features for accent classification
            acoustic_features = self._extract_accent_features(audio_path)
            
            # 4. Linguistic analysis of the text
            linguistic_features = self._analyze_linguistic_patterns(results["transcription"])
            
            # 5. Accent classification
            accent_prediction = self._predict_accent(acoustic_features, linguistic_features)
            results["accent_classification"] = accent_prediction["accent"]
            results["confidence_score"] = accent_prediction["confidence"]
            
            # 6. Generate explanation
            results["explanation"] = self._generate_explanation(
                accent_prediction, acoustic_features, linguistic_features
            )
            
        except Exception as e:
            results["explanation"] = f"Error during analysis: {str(e)}"
            
        return results
    
    def _transcribe_with_language_detection(self, audio_path):
        """Transcribes and detects language"""
        result = self.whisper_model.transcribe(audio_path)
        return result
    
    def _detect_english_confidence(self, transcription_result):
        """Detects if the audio is in English"""
        
        # Use Whisper's language detection
        detected_language = transcription_result.get("language", "unknown")
        
        if detected_language == "en":
            base_confidence = 0.8
        else:
            base_confidence = 0.2
            
        # Additional analysis using text patterns
        text = transcription_result.get("text", "").lower()
        
        # Common English words
        english_words = ["the", "and", "is", "in", "to", "of", "a", "that", "it", "with", "for", "as", "was", "on", "are"]
        english_word_count = sum(1 for word in english_words if word in text)
        
        # Adjust confidence based on English words
        word_confidence = min(english_word_count / 5, 1.0) * 0.3
        
        total_confidence = min(base_confidence + word_confidence, 1.0)
        return round(total_confidence, 2)
    
    def _extract_accent_features(self, audio_path):
        """Extracts acoustic features for accent classification"""
        
        y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)
        
        features = {}
        
        # Prosodic features (rhythm and intonation)
        # F0 (fundamental pitch)
        f0 = librosa.yin(y, fmin=50, fmax=300)
        f0_clean = f0[f0 > 0]
        
        features['f0_mean'] = float(np.mean(f0_clean)) if len(f0_clean) > 0 else 0
        features['f0_std'] = float(np.std(f0_clean)) if len(f0_clean) > 0 else 0
        features['f0_range'] = float(np.max(f0_clean) - np.min(f0_clean)) if len(f0_clean) > 0 else 0
        
        # Formants (vowel features)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()
        features['mfcc_std'] = np.std(mfccs, axis=1).tolist()
        
        # Temporal features
        features['speech_rate'] = self._estimate_speech_rate(y, sr)
        features['pause_ratio'] = self._estimate_pause_ratio(y, sr)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
        
        return features
    
    def _analyze_linguistic_patterns(self, text):
        """Analyzes linguistic patterns in the text"""
        
        patterns = {}
        text_lower = text.lower()
        
        # Indicators of different English accents
        
        # Americanisms
        american_words = ["elevator", "apartment", "gas", "truck", "mom", "candy", "fall", "gotten"]
        patterns['american_indicators'] = sum(1 for word in american_words if word in text_lower)
        
        # Briticisms
        british_words = ["lift", "flat", "petrol", "lorry", "mum", "sweets", "autumn", "whilst"]
        patterns['british_indicators'] = sum(1 for word in british_words if word in text_lower)
        
        # Australian/NZ
        aussie_words = ["mate", "fair dinkum", "no worries", "heaps", "arvo", "brekkie"]
        patterns['australian_indicators'] = sum(1 for word in aussie_words if word in text_lower)
        
        # Rhoticity patterns (pronunciation of 'r')
        r_words = re.findall(r'\b\w*r\w*\b', text_lower)
        patterns['r_word_count'] = len(r_words)
        
        # Average word length (some accents tend to use longer words)
        words = text.split()
        patterns['avg_word_length'] = np.mean([len(word) for word in words]) if words else 0
        patterns['total_words'] = len(words)
        
        return patterns
    
    def _predict_accent(self, acoustic_features, linguistic_features):
        """Predicts the accent based on features"""
        
        # Heuristic scoring system (use ML in a real implementation)
        scores = {accent: 0 for accent in self.accent_categories}
        
        # F0 (pitch) analysis
        f0_mean = acoustic_features.get('f0_mean', 0)
        
        if 120 <= f0_mean <= 180:  # Typical female range
            if f0_mean > 150:
                scores["Australian"] += 0.3
                scores["American"] += 0.2
        elif 80 <= f0_mean <= 120:  # Typical male range
            if f0_mean < 100:
                scores["British"] += 0.3
                scores["Scottish"] += 0.2
        
        # Linguistic analysis
        if linguistic_features['american_indicators'] > 0:
            scores["American"] += 0.4
            scores["Canadian"] += 0.2
            
        if linguistic_features['british_indicators'] > 0:
            scores["British"] += 0.4
            scores["Irish"] += 0.1
            
        if linguistic_features['australian_indicators'] > 0:
            scores["Australian"] += 0.5
            
        # Speech rate
        speech_rate = acoustic_features.get('speech_rate', 0)
        if speech_rate > 4:  # Words per second
            scores["American"] += 0.2
        elif speech_rate < 2.5:
            scores["British"] += 0.2
            scores["Irish"] += 0.1
            
        # If no clear indicators, classify as "Other"
        max_score = max(scores.values())
        if max_score < 0.3:
            scores["Other"] = 0.6
            
        # Find the accent with the highest score
        predicted_accent = max(scores, key=scores.get)
        confidence = min(scores[predicted_accent], 1.0)
        
        return {
            "accent": predicted_accent,
            "confidence": round(confidence, 2),
            "all_scores": scores
        }
    
    def _estimate_speech_rate(self, y, sr):
        """Estimates speech rate"""
        # Detect onsets (sound beginnings)
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        duration = len(y) / sr
        return len(onset_frames) / duration if duration > 0 else 0
    
    def _estimate_pause_ratio(self, y, sr):
        """Estimates pause ratio"""
        # Detect silent regions
        rms = librosa.feature.rms(y=y)[0]
        threshold = np.mean(rms) * 0.1
        silence_frames = np.sum(rms < threshold)
        return silence_frames / len(rms)
    
    def _generate_explanation(self, accent_prediction, acoustic_features, linguistic_features):
        """Generates explanation for the classification"""
        
        accent = accent_prediction["accent"]
        confidence = accent_prediction["confidence"]
        
        explanation = f"Accent classified as {accent} with {confidence*100:.1f}% confidence. "
        
        # Add specific details
        if accent == "American":
            explanation += "Indicators: American intonation patterns, "
            if linguistic_features['american_indicators'] > 0:
                explanation += "American vocabulary detected, "
                
        elif accent == "British":
            explanation += "Indicators: British prosodic features, "
            if linguistic_features['british_indicators'] > 0:
                explanation += "British vocabulary detected, "
                
        elif accent == "Australian":
            explanation += "Indicators: Australian intonation patterns, "
            if linguistic_features['australian_indicators'] > 0:
                explanation += "Australian expressions detected, "
        
        # Add technical information
        f0_mean = acoustic_features.get('f0_mean', 0)
        speech_rate = acoustic_features.get('speech_rate', 0)
        
        explanation += f"average pitch: {f0_mean:.1f}Hz, speech rate: {speech_rate:.1f} events/sec."
        
        return explanation
