import streamlit as st
from openai import OpenAI
import os

# Page configuration
st.set_page_config(
    page_title="Vilnius Travel Consultant - AI Chatbot",
    page_icon="🏛️",
    layout="wide"
)

# Title and description
st.title("🏛️ Vilnius Travel Consultant")
st.markdown("**AI pagalbininkas kelionėms po Vilnių** | Powered by Gemini 2.5 Flash")

# Sidebar for API key input
with st.sidebar:
    st.header("⚙️ Nustatymai / Settings")
    api_key = st.text_input(
        "OpenRouter API raktas:",
        type="password",
        help="Įveskite savo OpenRouter API raktą. Jūs galite jį gauti iš https://openrouter.ai"
    )
    
    if api_key:
        st.success("✅ API raktas įvestas!")
    else:
        st.warning("⚠️ Prašome įvesti API raktą")
    
    st.markdown("---")
    st.markdown("### 📝 Kaip naudotis:")
    st.markdown("""
    1. Įveskite OpenRouter API raktą
    2. Užduokite klausimą lietuviškai
    3. AI atsakys lietuviškai apie Vilnių
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Užduokite klausimą apie Vilnių... 🏛️"):
    if not api_key:
        st.error("⚠️ Prašome pirmiausia įvesti OpenRouter API raktą šoniniame meniu!")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        try:
            # Create OpenAI client for OpenRouter
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            
            # Prepare messages for API call
            messages_for_api = [
                {
                    "role": "system", 
                    "content": """Tu esi Vilniaus kelionių konsultantas. Visada atsakyk lietuviškai. 
                    Tavo tikslas - padėti žmonėms planuoti keliones po Vilnių ir suteikti informaciją apie miestą. 
                    Būk draugiškas, informatyvus ir naudojamas. Jei nežinai tikslaus atsakymo, pasakyk, kad nežinai, 
                    bet pasiūlyk alternatyvas ar bendras rekomendacijas apie Vilnių."""
                }
            ]
            
            # Add chat history (keeping last 10 messages for context)
            recent_messages = st.session_state.messages[-10:]
            for msg in recent_messages[:-1]:  # Exclude the current message as it's already in the input
                messages_for_api.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add current user message
            messages_for_api.append({
                "role": "user",
                "content": prompt
            })
            
            # Make API call with loading spinner
            with st.spinner("AI galvoja... 🤔"):
                completion = client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://vilnius-travel-consultant.streamlit.app",
                        "X-Title": "Vilnius Travel Consultant",
                    },
                    model="google/gemini-2.5-flash",
                    messages=messages_for_api,
                    temperature=0.7,
                    max_tokens=1000
                )
            
            # Get the response
            response = completion.choices[0].message.content
            
            # Display the response
            st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = f"❌ Klaida: {str(e)}"
            st.error(error_message)
            
            # Add error to chat history so user can see it
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: small;'>
    🏛️ Vilnius Travel Consultant | Sukurta su Streamlit ir OpenRouter AI
    </div>
    """, 
    unsafe_allow_html=True
)