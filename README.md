# 🏛️ Vilnius Travel Consultant

An AI-powered chatbot that helps plan trips to Vilnius, Lithuania. The bot uses OpenRouter AI with Gemini 2.5 Flash model and responds in Lithuanian to questions about Vilnius attractions, restaurants, hotels, and travel recommendations.

## Features

- 🤖 Powered by Gemini 2.5 Flash via OpenRouter AI
- 🇱🇹 Responds in Lithuanian language
- 🏛️ Specialized knowledge about Vilnius
- 💬 Interactive chat interface with Streamlit
- 🔐 Secure API key input
- 📱 Responsive web interface

## Quick Start

### Method 1: Using the Shell Script (Easiest)
```bash
cd /Users/virgilijus/Desktop/Projects/vilnius-travel-consultant
./start_chatbot.sh
```

### Method 2: Manual Setup
1. Create virtual environment: `python3 -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `streamlit run main.py`

## Prerequisites

- Python 3.9 or higher
- OpenRouter API key (get one at https://openrouter.ai)
- Internet connection

## Usage

1. Open http://localhost:8501 in your browser
2. Enter your OpenRouter API key in the sidebar
3. Start asking questions about Vilnius in Lithuanian!

## Example Questions (in Lithuanian)

- "Kokias vietas verta aplankyti Vilniuje?"
- "Kur geriausia pavalgyti Vilniaus senamiestyje?"
- "Kaip nuvykti iš oro uosto į centrą?"
- "Kokie yra geriausi viešbučiai Vilniuje?"

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Gemini 2.5 Flash (via OpenRouter)
- **Language**: Python 3.9+

## Files Structure

- `main.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `start_chatbot.sh` - Easy startup script
- `KAIP_PALEISTI.md` - Detailed instructions in Lithuanian
- `docs/` - Documentation and examples

## Support

For detailed Lithuanian instructions, see `KAIP_PALEISTI.md`.

## License

This project is open source and available under the MIT License. 
