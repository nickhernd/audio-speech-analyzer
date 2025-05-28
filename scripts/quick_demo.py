#!/usr/bin/env python3
"""
Quick demo of the English Accent Classifier
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo():
    print("English Accent Classifier - Quick Demo")
    print("=" * 45)
    print()
    print("This script demonstrates how to use the classifier:")
    print()
    
    # Show example code
    code_example = '''
from src.audio_processor import AudioProcessor
from src.accent_classifier import EnglishAccentClassifier

# 1. Process audio from URL
processor = AudioProcessor()
audio_path = processor.download_and_extract_audio("YOUR_VIDEO_URL")

# 2. Classify accent
classifier = EnglishAccentClassifier()
results = classifier.classify_accent(audio_path)

# 3. Show results
print(f"Accent: {results['accent_classification']}")
print(f"Confidence: {results['confidence_score']*100:.1f}%")
print(f"English Confidence: {results['english_confidence']*100:.1f}%")
'''
    
    print("Example code:")
    print(code_example)
    
    print("Command line usage:")
    print("python src/main.py --url 'YOUR_VIDEO_URL' --verbose")
    print()
    
    print("Supported accents:")
    accents = [
        "American", "British", "Australian", "Canadian",
        "Irish", "Scottish", "South African", "Indian", "Other"
    ]
    for i, accent in enumerate(accents, 1):
        print(f"  {i}. {accent}")
    
    print()
    print("Expected output:")
    print("LANGUAGE: English detected (87.5% confidence)")
    print("ACCENT: American")  
    print("CONFIDENCE: 78.3%")
    print("EXPLANATION: Accent classified as American...")

if __name__ == '__main__':
    demo()
