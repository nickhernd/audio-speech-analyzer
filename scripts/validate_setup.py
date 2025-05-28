#!/usr/bin/env python3
"""
Validates that all dependencies are correctly installed
"""
import sys
import importlib

def check_dependency(module_name, display_name=None):
    """Checks if a module is available"""
    if display_name is None:
        display_name = module_name
        
    try:
        importlib.import_module(module_name)
        print(f"{display_name}: OK")
        return True
    except ImportError:
        print(f"{display_name}: NOT FOUND")
        return False

def check_system_dependencies():
    """Checks system dependencies"""
    import subprocess
    
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        print("ffmpeg: OK")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ffmpeg: NOT FOUND")
        return False

def main():
    print("Validating English Accent Classifier installation")
    print("=" * 55)
    
    all_good = True
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"Python {python_version.major}.{python_version.minor}: OK")
    else:
        print(f"Python {python_version.major}.{python_version.minor}: Requires 3.8+")
        all_good = False
    
    print("\nChecking Python dependencies:")
    
    # Critical dependencies
    deps = [
        ('librosa', 'librosa (audio processing)'),
        ('whisper', 'openai-whisper (speech recognition)'),
        ('yt_dlp', 'yt-dlp (video download)'),
        ('sklearn', 'scikit-learn (machine learning)'),
        ('click', 'click (CLI interface)'),
        ('numpy', 'numpy (numerical computing)'),
        ('pandas', 'pandas (data processing)'),
        ('soundfile', 'soundfile (audio I/O)'),
    ]
    
    for module, display in deps:
        if not check_dependency(module, display):
            all_good = False
    
    print("\nChecking system dependencies:")
    if not check_system_dependencies():
        all_good = False
    
    print("\n" + "=" * 55)
    if all_good:
        print("All set up correctly!")
        print("\nYou can run:")
        print("   python src/main.py --url 'YOUR_VIDEO_URL' --verbose")
    else:
        print("There are problems with the installation")
        print("\nTo fix:")
        print("   1. pip install -r requirements.txt")
        print("   2. Install ffmpeg on your system")
        
    return 0 if all_good else 1

if __name__ == '__main__':
    sys.exit(main())
