#!/usr/bin/env python3
"""
English Accent Classifier - Main script for English accent classification
"""
import click
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.audio_processor import AudioProcessor
from src.accent_classifier import EnglishAccentClassifier
from config.settings import *

@click.command()
@click.option('--url', required=True, help='URL of the video to analyze')
@click.option('--output', default='accent_results.json', help='Output file')
@click.option('--verbose', is_flag=True, help='Verbose mode')
def classify_accent(url, output, verbose):
    """Classifies the English accent from a video URL"""
    
    click.echo("English Accent Classifier")
    click.echo("=" * 50)
    
    if verbose:
        click.echo(f"Analyzing video: {url}")
    
    try:
        # 1. Process audio
        click.echo("Downloading and extracting audio...")
        processor = AudioProcessor()
        audio_path = processor.download_and_extract_audio(url)
        
        if verbose:
            click.echo(f"Audio extracted: {audio_path}")
        
        # 2. Classify accent
        click.echo("Analyzing English accent...")
        classifier = EnglishAccentClassifier()
        results = classifier.classify_accent(audio_path)
        
        # 3. Show main results
        click.echo("\n" + "="*50)
        click.echo("CLASSIFICATION RESULTS")
        click.echo("="*50)
        
        # Check if English
        if results['english_confidence'] < 0.7:
            click.echo(f"LANGUAGE: Not detected as English")
            click.echo(f"English confidence: {results['english_confidence']*100:.1f}%")
            click.echo(f"Explanation: {results['explanation']}")
        else:
            click.echo(f"LANGUAGE: English detected ({results['english_confidence']*100:.1f}% confidence)")
            click.echo(f"ACCENT: {results['accent_classification']}")
            click.echo(f"CONFIDENCE: {results['confidence_score']*100:.1f}%")
            click.echo(f"EXPLANATION: {results['explanation']}")
        
        if verbose:
            click.echo("\n" + "-"*30)
            click.echo("TRANSCRIPTION:")
            click.echo(f'"{results["transcription"][:200]}..."' if len(results["transcription"]) > 200 else f'"{results["transcription"]}"')
        
        # 4. Save full results
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        click.echo(f"\nFull results saved to: {output}")
        
        # 5. Final summary
        click.echo("\n" + "="*50)
        if results['accent_classification'] and results['confidence_score'] > 0.5:
            click.echo(f"RESULT: {results['accent_classification']} accent detected!")
        else:
            click.echo("RESULT: Could not reliably classify English accent")
        click.echo("="*50)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    classify_accent()
