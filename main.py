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
st.info("ℹ️ Šis chatbot'as naudoja tik specialiai paruoštus duomenis apie 9 svarbiausias Vilniaus vietas ir jų istoriją.")

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
    st.markdown("### 🏛️ Galimos temos:")
    st.markdown("""
    - **Stiklo kvartalas** - auksakalių kvartalas
    - **Gedimino pilis** - simbolis su apžvalgos aikštele  
    - **Užupio respublika** - menininkų rajonas
    - **Žvėryno rajonas** - 108 mediniai namai
    - **Onos bažnyčia** - gotikos šedevras
    - **Vilniaus katedra** - krikšto simbolis
    - **Aušros vartai** - gynybiniai vartai su Madona
    - **Užutrakio sodyba** - dvaras prie ežero
    - **Verkių dvaras** - "Vilniaus Versalis"
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
                    SVARBU: Naudok TIKTAI žemiau pateiktą informaciją apie Vilnių. NEGALIMA naudoti jokių kitų šaltinių ar žinių. 
                    Jei klausimas nėra susijęs su pateikta informacija, pasakyk, kad neturi informacijos apie tai.
                    
                    VILNIAUS INFORMACIJA:
                    
                    STIKLO KVARTALAS:
                    Stiklo kvartalas susikūrė 2018-ųjų spalį Stiklių, M. Antokolskio, Gaono ir Žydų gatvių teritorijoje. Jau daugiau nei 600 metų skaičiuojantis kvartalas buvo žydų gyvenamoji vieta, auksakalių, stiklapūčių, amatininkų ir finansininkų miestelis. 1495 m. čia buvo įkurta auksakalių gildija, 1547 m. – pirmoji LDK stiklo manufaktūra. Iki šiol glaudžia juvelyrus, vietos menininkų krautuvėles ir dirbtuves, jaukius restoranus, kamerinį orkestrą, meno galerijas ir viešbutį „Stikliai".

                    GEDIMINO PILIS:
                    Gedimino pilies bokštas - lankomiausias Lietuvos nacionalinio muziejaus padalinys. Vienintelis išlikęs Aukštutinės pilies įtvirtinimo bokštas. Pirmiausia buvo medinė pilis, 1409 m. Vytautas Didysis pastatė mūrinę pilį. Bokšte istorinė paroda su Vilniaus pilių rekonstrukcijos modeliais, ginkluote. Antrame aukšte interaktyvi ekspozicija „Laiko juostos vaizdai pro Gedimino pilies bokšto langus". Trečiame aukšte - apie Baltijos kelią 1989 m. Bokšto apžvalgos aikštelė atskleidžia Vilniaus panoramą.

                    UŽUPIO RESPUBLIKA:
                    Menininkų respublika su nuosavu himnu, konstitucija (Paupio gatvės pradžioje ant tvoros), prezidentu, vyskupu. Vienas seniausių Vilniaus rajonų (minimas XVI a.). Senovėje buvo malūnų ir vargingųjų priemiestis. Simboliai: bronzinė undinėlė (Užupio mergelė, skulpt. Romas Vilčiauskas) ir Angelo skulptūra (2002 m., centr. aikštėje). Sovietmečiu apleistas, dabar prestižiškas rajonas su festivaliais, koncertais, parodomis.

                    ŽVĖRYNO RAJONAS:
                    XVI-XIX a. priklausė Radviloms, turėjusiems žvėrių medžioklės rezervatą. 108 mediniai namai su šveicariškais bokšteliais, rusiško stiliaus langų apvadais, tradicine lietuviška ornamentika. Žvėryno tvenkiniai (nuo XVI a.), tiltas į Vingio parką. Šalia Liubarto tilto - karaimų kenesa, stačiatikių Švč. Mergelės Marijos cerkvė (1903 m.).

                    ONOS BAŽNYČIA:
                    Šv. Onos bažnyčia - vėlyvosios gotikos šedevras, per penkis šimtmečius beveik nepakitusi. Legenda: Napoleonas norėjo ją nusinešti į Paryžių. Šalia XIX a. varpinė, imituojanti gotikos stilių. Bernardinų istorinis-architektūrinis ansamblis su Šv. Pranciškaus Asyžiečio bažnyčia ir vienuolynu (XV a.). Vienuolyno gotikinis interjeras, žvaigždiniai ir kryžminiai skliautai.

                    VILNIAUS KATEDRA:
                    Šv. Stanislovo ir Šv. Vladislovo arkikatedra bazilika - Lietuvos krikšto simbolis. Pastatyta buvusios pagonių šventyklos vietoje. Čia ilsisi Šv. Kazimiero palaikai. Klasicistinio stiliaus (architektas Laurynas Stuoka-Gucevičius), bet mūruose gotikos, renesanso, baroko pėdsakai. 57 m varpinės bokštas (XIII a. pradžia, gynybinis bokštas, XVI a. tapo varpine). Viršuje seniausias miesto laikrodis.

                    AUŠROS VARTAI:
                    Vieninteliai išlikę iš 10 miesto gynybinių vartų (paminėti 1514 m.). Pradžioje vadinti Medininkų vartais. Koplyčioje stebuklingas Švenčiausiosios Mergelės Marijos paveikslas (XVII a., pagal Martino de Voso pavyzdį), vadinamas Aušros Vartų Madona ar Vilniaus Madona. Garbino katalikai, stačiatikiai, unitai.

                    UŽUTRAKIO SODYBA:
                    Ant Galvės ežero kranto. XX a. pradžioje įkūrė grafas Juozapas Tiškevičius su žmona Jadvyga. Patenkama plaustu per ežerų sąsmauką (sausumos kelias - tik ūkiui, vadintas Bulvių keliu). Rūmus kūrė architektas Juzefas Husas, parką - Eduardas Fransua Andrė. Mišraus stiliaus parkas su antikinių skulptūrų kopijomis, beveik 100 rūšių medžiai ir krūmai.

                    VERKIŲ DVARAS:
                    Vilniaus pakraštyje prie Neries upės. Stačiuose šlaituose kelių šimtų metų ąžuolai (1,5 m skersmens). Kadaise šventas ąžuolynas - didžiųjų kunigaikščių valda. XIV a. pabaigos rūmai - "Vilniaus Versalis". 1786 m. oranžerijos su tropiniais augalais iš Italijos. Po Lietuvos krikšto Jogaila užrašė vyskupams. Architektas Martynas Knakfusas ir Laurynas Stuoka-Gucevičius sukūrė klasicistinį ansamblį.
                    
                    Atsakyk TIKTAI remiantis šia informacija. Jei klausiama apie ką nors, ko nėra šioje informacijoje, pasakyk: "Atsiprašau, neturiu informacijos apie tai savo duomenų bazėje. Galiu papasakoti apie: Stiklo kvartalą, Gedimino pilį, Užupio respubliką, Žvėryno rajoną, Onos bažnyčią, Vilniaus katedrą, Aušros vartus, Užutrakio sodybą arba Verkių dvarą."
                    """
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