import os
import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TravelBot | Travel Assistant",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """ <style>
.hero {
    padding: 2rem 1.5rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #e8f5ff 0%, #f7fbff 100%);
    border: 1px solid #d9ecff;
}

.hero h1 {
    margin: 0;
    font-size: 3rem;
}

.hero p {
    margin: 0.45rem 0 0 0;
    font-size: 1.05rem;
}

.muted {
    color: #667085;
    font-size: 0.92rem;
}

.card {
    padding: 1.1rem;
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-radius: 16px;
    min-height: 125px;
    background: rgba(255, 255, 255, 0.55);
    margin-bottom: 0.8rem;
}

.card h3 {
    margin-top: 0;
    margin-bottom: 0.7rem;
}

.section-title {
    margin-top: 1.4rem;
    margin-bottom: 0.4rem;
}

section[data-testid="stSidebar"] .stButton button {
    margin-bottom: 0.25rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# GROQ API KEY
# =========================================================

def get_api_key():
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")

api_key = get_api_key()

if not api_key:
    st.error(
        "Groq API key is not configured. "
        "For local use, set GROQ_API_KEY. "
        "For Streamlit Cloud, add GROQ_API_KEY in App settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"

# =========================================================
# DESTINATION DATA
# =========================================================

DESTINATIONS = {
    "🏖️ Beach": [
        {
            "name": "Goa",
            "description": (
                "Beaches, coastal villages, nightlife and "
                "Portuguese-influenced heritage."
            ),
            "tag": "Beach • Food • Heritage",
        },
        {
            "name": "Andaman Islands",
            "description": (
                "Tropical beaches, clear water, island scenery "
                "and water activities."
            ),
            "tag": "Island • Nature • Water",
        },
        {
            "name": "Varkala",
            "description": (
                "Clifftop coastal views, beaches, wellness "
                "experiences and a relaxed atmosphere."
            ),
            "tag": "Cliff • Beach • Relaxed",
        },
    ],
    "🏙️ City": [
        {
            "name": "Delhi",
            "description": (
                "A mix of historic monuments, museums, markets "
                "and modern city life."
            ),
            "tag": "History • Food • City",
        },
        {
            "name": "Mumbai",
            "description": (
                "A major coastal city known for landmarks, food, "
                "cinema and urban culture."
            ),
            "tag": "Coast • Culture • City",
        },
        {
            "name": "Bengaluru",
            "description": (
                "A technology hub with parks, cafés, museums "
                "and a lively food scene."
            ),
            "tag": "Tech • Food • Parks",
        },
    ],
    "🌿 Nature": [
        {
            "name": "Munnar",
            "description": (
                "Hill landscapes, tea plantations, viewpoints "
                "and cool weather."
            ),
            "tag": "Hills • Tea • Nature",
        },
        {
            "name": "Coorg",
            "description": (
                "Coffee plantations, forests, waterfalls and "
                "scenic hill-country experiences."
            ),
            "tag": "Coffee • Hills • Waterfalls",
        },
        {
            "name": "Ooty",
            "description": (
                "A popular hill station with gardens, lakes, "
                "viewpoints and colonial-era charm."
            ),
            "tag": "Hill Station • Gardens • Lakes",
        },
    ],
    "🏔️ Adventure": [
        {
            "name": "Rishikesh",
            "description": (
                "Known for river activities, trekking, yoga "
                "and Himalayan foothill scenery."
            ),
            "tag": "River • Trekking • Outdoors",
        },
        {
            "name": "Manali",
            "description": (
                "A Himalayan destination for mountain scenery, "
                "outdoor activities and road trips."
            ),
            "tag": "Mountains • Snow • Adventure",
        },
        {
            "name": "Kedarnath",
            "description": (
                "A high-altitude pilgrimage destination reached "
                "through a Himalayan trekking route."
            ),
            "tag": "Pilgrimage • Himalayas • Trek",
        },
    ],
    "🏛️ Cultural": [
        {
            "name": "Tirupati",
            "description": (
                "A major pilgrimage destination centered around "
                "the Sri Venkateswara Temple."
            ),
            "tag": "Temple • Pilgrimage • Culture",
        },
        {
            "name": "Varanasi",
            "description": (
                "A historic city on the Ganges known for temples, "
                "ghats and cultural traditions."
            ),
            "tag": "Heritage • Ghats • Culture",
        },
        {
            "name": "Jaipur",
            "description": (
                "The Pink City, known for forts, palaces, "
                "markets and Rajasthani heritage."
            ),
            "tag": "Forts • Palaces • Heritage",
        },
    ],
}

# =========================================================
# AI SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are TravelBot, a travel assistant.
Your role is to help users with travel-related questions and trip planning.

You can discuss:
* Destinations and sightseeing
* Itineraries
* Best seasons and weather considerations
* Transportation
* Accommodation types
* Approximate budgets
* Packing
* Local customs
* Pilgrimage travel
* Food and activities
* Practical travel planning tips

Do not answer unrelated questions such as:
* Programming
* Java
* C
* Python
* Mathematics
* General academic questions

For unrelated questions, reply briefly:
"Sorry, I am TravelBot and I only answer travel-related questions."

Be practical, clear and concise.
Do not present uncertain current prices, schedules, opening dates,
weather, visa rules or safety conditions as guaranteed facts.
When information may change, advise the user to verify it with official sources.
"""

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "🏖️ Beach"

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None

# =========================================================
# AI FUNCTION
# =========================================================

def ask_groq(user_message, extra_context=""):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if extra_context:
        messages.append(
            {
                "role": "system",
                "content": extra_context,
            }
        )

    messages.extend(st.session_state.messages[-12:])

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5,
        max_completion_tokens=1200,
    )

    return response.choices[0].message.content

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """ <div class="hero"> <h1>🌍 TravelBot</h1> <p>Plan smarter. Discover places. Travel better.</p> </div> """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.header("🧭 Explore")

    theme = st.selectbox(
        "Choose a travel type",
        list(DESTINATIONS.keys()),
        index=list(DESTINATIONS.keys()).index(
            st.session_state.selected_theme
        ),
    )

    st.session_state.selected_theme = theme

    st.divider()

    st.subheader("💬 Quick Travel Ideas")

    quick_questions = [
        "Plan a 3-day trip to Goa",
        "Best places to visit in Munnar",
        "Suggest a budget trip from Hyderabad",
        "Best time to visit Manali",
        "Plan a family trip to Jaipur",
    ]

    for index, question in enumerate(quick_questions):
        if st.button(
            question,
            use_container_width=True,
            key=f"quick_question_{index}",
        ):
            st.session_state.quick_question = question
            st.rerun()

    st.divider()

    st.subheader("🗑️ Conversation")

    if st.button(
        "Clear Chat History",
        use_container_width=True,
        key="clear_chat_history",
    ):
        st.session_state.messages = []
        st.session_state.quick_question = None
        st.rerun()

# =========================================================
# DESTINATION SECTION
# =========================================================

st.subheader(f"{theme} Destinations")

destinations = DESTINATIONS[theme]

columns = st.columns(3)

for index, (column, destination) in enumerate(
    zip(columns, destinations)
):
    with column:
        st.markdown(
            f"""
            <div class="card">
                <h3>📍 {destination["name"]}</h3>
                <p>{destination["description"]}</p>
                <p class="muted">
                    <strong>{destination["tag"]}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"Ask about {destination['name']}",
            key=f"ask_destination_{index}",
            use_container_width=True,
        ):
            st.session_state.quick_question = (
                f"Tell me about {destination['name']} "
                f"and suggest a simple travel plan."
            )
            st.rerun()

# =========================================================
# TRAVEL ASSISTANT
# =========================================================

st.markdown(
    '<h2 class="section-title">🤖 Travel Assistant</h2>',
    unsafe_allow_html=True,
)

st.write(
    "Ask about destinations, itineraries, budgets, transportation, "
    "food, activities and travel planning."
)

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# PROCESS QUICK QUESTION
# =========================================================

if st.session_state.quick_question:
    question = st.session_state.quick_question
    st.session_state.quick_question = None

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    context = (
        f"The user is currently exploring the travel category: {theme}."
    )

    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            try:
                answer = ask_groq(question, context)
                st.markdown(answer)
            except Exception:
                answer = (
                    "Sorry, I couldn't generate a response right now. "
                    "Please check your Groq API configuration and try again."
                )
                st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

# =========================================================
# NORMAL CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask TravelBot about your next trip..."
)

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    context = (
        f"The user is currently exploring the travel category: {theme}."
    )

    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            try:
                answer = ask_groq(user_input, context)
                st.markdown(answer)
            except Exception:
                answer = (
                    "Sorry, I couldn't generate a response right now. "
                    "Please check your Groq API configuration and try again."
                )
                st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )