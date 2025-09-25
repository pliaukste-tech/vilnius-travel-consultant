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
        help="Įveskite savo OpenRouter API raktą. Jūs galite jį gauti iš https://openrouter.ai",
        placeholder="sk-or-v1-..."
    )
    
    if api_key:
        # Basic API key format validation
        if api_key.startswith("sk-or-v1-") and len(api_key) > 20:
            st.success("✅ API raktas įvestas!")
            
            # Test API connection button
            if st.button("🔍 Patikrinti API ryšį"):
                try:
                    with st.spinner("Tikrinamas API raktas..."):
                        # Create test client
                        test_client = OpenAI(
                            base_url="https://openrouter.ai/api/v1",
                            api_key=api_key,
                        )
                        
                        # Make a simple test request
                        test_completion = test_client.chat.completions.create(
                            model="google/gemini-2.5-flash",
                            messages=[{"role": "user", "content": "Hi"}],
                            max_tokens=5
                        )
                        
                        st.success("✅ API raktas veikia! Galite pradėti pokalbį.")
                        
                except Exception as e:
                    if "401" in str(e):
                        st.error("❌ API raktas neteisingas. Patikrinkite ir pabandykite iš naujo.")
                    else:
                        st.error(f"❌ Ryšio klaida: {str(e)}")
        else:
            st.warning("⚠️ API rakto formatas atrodo neteisingas. Turėtų prasidėti 'sk-or-v1-'")
    else:
        st.warning("⚠️ Prašome įvesti API raktą")
    
    st.markdown("---")
    st.markdown("### 📝 Kaip naudotis:")
    st.markdown("""
    1. Įveskite OpenRouter API raktą
    2. Užduokite klausimą lietuviškai
    3. AI atsakys lietuviškai apie Vilnių
    """)
    
    st.markdown("---")
    st.markdown("### 🔑 API rakto gavimas:")
    st.markdown("""
    1. Eikite į [OpenRouter.ai](https://openrouter.ai)
    2. Užsiregistruokite/prisijunkite
    3. Eikite į "Keys" skyrių
    4. Sukurkite naują API raktą
    5. Nukopijuokite visą raktą (prasideda 'sk-or-v1-')
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
    
    # Validate API key format
    if not api_key.startswith("sk-or-v1-"):
        st.error("⚠️ API raktas turi prasidėti 'sk-or-v1-'. Patikrinkite, ar nukopijuote visą raktą.")
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
            error_str = str(e)
            
            # Provide specific error messages for common issues
            if "401" in error_str:
                if "User not found" in error_str or "Invalid API key" in error_str:
                    error_message = """❌ **API rakto klaida!** 
                    
**Galimos priežastys:**
- API raktas neteisingas arba pasenęs
- API raktas nukopijuotas ne pilnai
- Paskyra OpenRouter neaktyvi arba neturi kreditų

**Kaip išspręsti:**
1. Eikite į [OpenRouter.ai](https://openrouter.ai)
2. Patikrinkite, ar jūsų paskyra aktyvi
3. Sukurkite naują API raktą
4. Įsitikinkite, kad kopijuojate visą raktą (prasideda 'sk-or-v1-')
5. Patikrinkite, ar turite pakankamai kreditų paskyroje"""
                else:
                    error_message = f"❌ Autentifikacijos klaida (401): {error_str}"
            elif "429" in error_str:
                error_message = "❌ Per daug užklausų. Pabandykite po kelių minučių."
            elif "500" in error_str or "502" in error_str or "503" in error_str:
                error_message = "❌ OpenRouter serverio klaida. Pabandykite vėliau."
            elif "timeout" in error_str.lower():
                error_message = "❌ Užklausa per ilgai vykdoma. Pabandykite trumpesnį klausimą."
            else:
                error_message = f"❌ Klaida: {error_str}"
            
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