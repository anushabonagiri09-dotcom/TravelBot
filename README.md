# 🌍 TravelBot — AI Travel Assistant

TravelBot is a Streamlit-based AI travel assistant powered by the Groq API.

## Features

- 🏖️ Beach, city, nature, adventure and cultural themes
- 📍 Curated destination cards
- ✨ AI-generated destination guides
- 💬 Conversational travel chatbot
- 🧭 Itinerary, transport, budget and packing guidance
- 🗑️ Clear-chat control
- 🔐 API key stored outside source code
- ☁️ Ready for Streamlit Community Cloud deployment

## Tech Stack

- Python
- Streamlit
- Groq API
- OpenAI GPT-OSS 120B through Groq

## Run locally

### 1. Create/activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Create:

```text
.streamlit/secrets.toml
```

with:

```toml
GROQ_API_KEY = "your-new-groq-api-key"
```

Do not commit that file.

### 4. Start the app

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Create a new app.
4. Select your repository and `app.py`.
5. Open **Advanced settings → Secrets**.
6. Add:

```toml
GROQ_API_KEY = "your-new-groq-api-key"
```

7. Deploy.

## Security

Never put a real Groq API key inside `app.py`, `README.md`, screenshots,
or GitHub commits. If a key has already been exposed, revoke it and create
a new one.

## Example questions

- Tell me about Kedarnath
- Plan a 3-day trip to Goa
- What is the best time to visit Munnar?
- How can I reach Tirupati?
- Give me a budget estimate for Jaipur
- What should I pack for a Himalayan trip?

## Project structure

```text
TravelBot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Portfolio description

**TravelBot — AI Travel Assistant**

A Streamlit-based AI travel chatbot that uses the Groq API to provide
destination recommendations, travel guides, itinerary ideas, transport
information, budget guidance and practical travel tips.
