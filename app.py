"""
Zenith AI - Multi-Persona Intelligent Chatbot
Built with Streamlit & Google Gemini 2.5 Flash
For MuLearn 'Build a Simple Chatbot' Task (250 Karma Points)
"""

import os
import json
import streamlit as st
from personas import PERSONAS
from bot_engine import stream_gemini_chat, get_offline_response, GENAI_AVAILABLE

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Zenith AI - Smart Chatbot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, modern chat interface
st.markdown("""
<style>
    /* Global styles */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366F1, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .persona-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #A5B4FC;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .welcome-card {
        padding: 1.5rem;
        background: #1E293B;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1.5rem;
    }
    .stButton button {
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        border-color: #6366F1;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = list(PERSONAS.keys())[0]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ---------------------------------------------------------
# Resolve API Key
# ---------------------------------------------------------
def get_effective_api_key(user_input_key: str) -> str:
    """Checks UI input, Streamlit secrets, then environment variable."""
    if user_input_key.strip():
        return user_input_key.strip()
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Zenith AI")
    st.caption("Adaptive Multi-Persona Conversational Companion")
    st.divider()

    # Persona Selection
    chosen_persona = st.selectbox(
        "🎭 Select Persona",
        options=list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.selected_persona)
    )

    if chosen_persona != st.session_state.selected_persona:
        st.session_state.selected_persona = chosen_persona
        st.rerun()

    persona_info = PERSONAS[st.session_state.selected_persona]
    st.info(f"**Role**: {persona_info['description']}")

    st.divider()

    # API Configuration
    st.markdown("### 🔑 API Configuration")
    manual_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="AIzaSy...",
        help="Free key from https://aistudio.google.com/. Also supports Streamlit secrets & env vars."
    )
    api_key = get_effective_api_key(manual_key)

    if api_key:
        st.success("🟢 API Key Active (Live Gemini Mode)")
    else:
        st.warning("🟡 Offline / Demo Mode (No API key detected)")
        st.caption("The bot will use its built-in knowledge engine until an API key is provided.")

    # Model Settings
    with st.expander("⚙️ Model Parameters", expanded=False):
        model_name = st.selectbox(
            "Model Version",
            options=["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"],
            index=0
        )
        temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Higher values make responses more creative; lower values make them focused and deterministic."
        )

    st.divider()

    # Session Management
    st.markdown("### 📂 Session Controls")
    col_clear, col_export = st.columns(2)
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

    with col_export:
        if st.session_state.messages:
            # Prepare export format
            chat_export = {
                "persona": st.session_state.selected_persona,
                "history": st.session_state.messages
            }
            json_str = json.dumps(chat_export, indent=2)
            st.download_button(
                label="📥 Export",
                data=json_str,
                file_name="zenith_chat_history.json",
                mime="application/json",
                use_container_width=True
            )

    st.divider()
    st.caption("MuLearn Task: Build a Simple Chatbot (⭐ 250 Karma)")


# ---------------------------------------------------------
# Main Chat Area
# ---------------------------------------------------------
current_persona = PERSONAS[st.session_state.selected_persona]

# Main Title Header
st.markdown(f'<div class="main-header">⚡ Zenith AI Chatbot</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="persona-badge">{current_persona["avatar"]} Active Persona: {st.session_state.selected_persona}</div>',
    unsafe_allow_html=True
)

# Empty State: Welcome banner and quick starter questions
if len(st.session_state.messages) == 0:
    st.markdown(f"""
    <div class="welcome-card">
        <h3>{current_persona['avatar']} {current_persona['welcome']}</h3>
        <p style="color: #94A3B8; margin-bottom: 0;">
            Select a starter question below or type your own question in the chat bar to begin!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 💡 Try asking:")
    starter_cols = st.columns(2)
    for idx, starter in enumerate(current_persona["starters"]):
        col = starter_cols[idx % 2]
        with col:
            if st.button(starter, key=f"starter_{idx}", use_container_width=True):
                st.session_state.pending_prompt = starter
                st.rerun()

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar=current_persona["avatar"]):
            st.markdown(message["content"])

# ---------------------------------------------------------
# Input Handling & Response Generation
# ---------------------------------------------------------
chat_input_val = st.chat_input(f"Message Zenith ({st.session_state.selected_persona})...")

# Check if a starter was clicked or text was entered
active_prompt = None
if st.session_state.pending_prompt:
    active_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
elif chat_input_val:
    active_prompt = chat_input_val

if active_prompt:
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(active_prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": active_prompt
    })

    # 2. Display Assistant Streaming Response
    with st.chat_message("assistant", avatar=current_persona["avatar"]):
        if api_key:
            # Live streaming from Google Gemini
            response_generator = stream_gemini_chat(
                api_key=api_key,
                messages=st.session_state.messages[:-1],  # prior history
                user_prompt=active_prompt,
                system_instruction=current_persona["system_instruction"],
                model_name=model_name,
                temperature=temperature
            )
            full_response = st.write_stream(response_generator)
        else:
            # Intelligent offline fallback
            response_generator = get_offline_response(
                prompt=active_prompt,
                persona_name=st.session_state.selected_persona
            )
            full_response = st.write_stream(response_generator)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })
