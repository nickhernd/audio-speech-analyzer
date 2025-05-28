#!/bin/bash

echo "🧪 Testing English Accent Classifier"
echo "===================================="

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "📝 Testing with sample URLs (replace with real URLs):"
echo ""

# Test 1: American accent (ejemplo)
echo "🇺🇸 Test 1: American accent example"
echo "python src/main.py --url 'AMERICAN_ACCENT_URL' --verbose"
echo ""

# Test 2: British accent (ejemplo)  
echo "🇬🇧 Test 2: British accent example"
echo "python src/main.py --url 'BRITISH_ACCENT_URL' --verbose"
echo ""

# Test 3: Other accent (ejemplo)
echo "🌍 Test 3: Other accent example"  
echo "python src/main.py --url 'OTHER_ACCENT_URL' --verbose"
echo ""

echo "💡 Replace the URLs above with real video URLs to test"
echo "📋 Expected output format:"
echo "   ✅ Language: English detected (XX% confidence)"
echo "   🗣️  Accent: [American/British/Australian/etc.]"  
echo "   📊 Confidence: XX%"
echo "   💬 Explanation: [Technical reasoning]"
