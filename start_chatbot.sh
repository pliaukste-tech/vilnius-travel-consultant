#!/bin/bash

echo "🏛️ Vilnius Travel Consultant - Paleidimas..."
echo "========================================"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Klaida: main.py failas nerastas!"
    echo "Prašome paleisti šią komandą iš projekto folderio."
    exit 1
fi

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Kuriama virtuali aplinka..."
    python3 -m venv .venv
fi

echo "🔧 Aktyvuojama virtuali aplinka..."
source .venv/bin/activate

# Install requirements
echo "📚 Diegiamos reikalingos bibliotekos..."
pip install -r requirements.txt

echo "🚀 Paleidžiamas chatbot..."
echo "Naršyklėje atidarykite: http://localhost:8501"
echo "Sustabdyti chatbot: Ctrl+C"
echo ""

streamlit run main.py
