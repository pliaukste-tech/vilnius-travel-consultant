# 🏛️ Vilnius Travel Consultant - Paleidimo Instrukcijos

## Kas tai yra?
Tai yra AI chatbot'as, kuris padeda planuoti keliones po Vilnių. Jis naudoja OpenRouter AI su Gemini 2.5 Flash modeliu ir atsakinėja lietuviškai į klausimus apie Vilniaus lankytinas vietas, restoranų, viešbučių ir kitų rekomendacijas.

## 📋 Kas reikalinga prieš pradedant

### 1. Python (jei dar neturite)
- Atidarykite Terminal programą (rasite Applications > Utilities > Terminal)
- Įveskite komandą: `python3 --version`
- Jei matote Python versiją (pvz., "Python 3.11.0"), tada Python jau įdiegtas
- Jei ne, eikite į https://python.org ir atsisiųskite Python 3.9 arba naujesnę versiją

### 2. OpenRouter API raktas
1. Eikite į https://openrouter.ai
2. Užsiregistruokite arba prisijunkite
3. Eikite į "API Keys" skyrių
4. Sukurkite naują API raktą
5. Nukopijuokite ir išsaugokite šį raktą (jums reikės jo vėliau)

## 🚀 Kaip paleisti chatbot'ą

### 1. Atidarykite Terminal
- Spauskite Command + Space
- Parašykite "Terminal" ir paspauskite Enter

### 2. Pereikite į projektą folderį
```bash
cd /Users/virgilijus/Desktop/Projects/vilnius-travel-consultant
```

### 3. Sukurkite Python virtualų aplinką (tik pirmą kartą)
```bash
python3 -m venv .venv
```

### 4. Aktyvuokite virtualią aplinką
```bash
source .venv/bin/activate
```
*Pastaba: Matytės (.venv) prieš jūsų komandų eilutę - tai reiškia, kad virtuali aplinka aktyvi*

### 5. Įdiekite reikalingas bibliotekas (tik pirmą kartą arba kai jas atnaujinate)
```bash
pip install -r requirements.txt
```

### 6. Paleiskite chatbot'ą
```bash
streamlit run main.py
```

### 7. Naudojimasis
- Jūsų naršyklėje automatiškai atsidars http://localhost:8501
- Jei neatsidaro automatiškai, eikite į šį adresą naršyklėje
- Šoniniame meniu įveskite savo OpenRouter API raktą
- Pradėkite užduoti klausimus lietuviškai!

## 🛑 Kaip sustabdyti chatbot'ą
- Terminal lange spauskite Ctrl + C
- Uždarykite naršyklės skirtuką

## 📝 Naudojimo pavyzdžiai

Galite užduoti tokius klausimus:
- "Kokias vietas verta aplankyti Vilniuje?"
- "Kur geriausia pavalgyti Vilniaus senamiestyje?"
- "Kaip nuvykti iš oro uosto į centrą?"
- "Kokie yra geriausi viešbučiai Vilniuje?"
- "Ką veikti Vilniuje žiemą?"

## ❓ Jei kyla problemų

### Klaida: "python3: command not found"
- Python nėra įdiegtas. Atsisiųskite iš https://python.org

### Klaida: "streamlit: command not found"
- Virtuali aplinka neaktyvi arba bibliotekos neįdiegtos
- Pakartokite 4 ir 5 žingsnius

### Klaida: "Import error" arba "Module not found"
- Įvykdykite: `pip install -r requirements.txt`

### API klaidos
- Patikrinkite, ar teisingai įvedėte OpenRouter API raktą
- Patikrinkite, ar turite pakankamai kreditų OpenRouter paskyroje

### Lietuviškos raidės neveikia
- Šis chatbot'as palaiko lietuviškas raides (ą, č, ę, ė, į, š, ų, ū, ž)
- Jei vis tiek yra problemų, patikrinkite Terminal kodavimą

## 💡 Patarimai MacBook Air naudotojams
- Uždarykite kitas programas, kad atlaisvintumėte atminties
- Jei kompiuteris šyla, AI atsakymų generavimas gali trukti ilgiau
- Internetinis ryšys turi būti stabilus, nes AI veikia debesyje

## 🔧 Papildomi Terminal patarimai
- Kad matytumėte failų sąrašą: `ls`
- Kad pamatytumėte, kuriame folderyje esate: `pwd`
- Kad išeitumėte iš virtualios aplinkos: `deactivate`

Sėkmės naudojantis Vilnius Travel Consultant! 🏛️