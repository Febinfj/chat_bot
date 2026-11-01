# ⚡ Zenith AI — Intelligent Multi-Persona Chatbot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20GenAI-Gemini%202.5%20Flash-4285F4?logo=google&logoColor=white)](https://aistudio.google.com/)
[![MuLearn](https://img.shields.io/badge/%C2%B5Learn-250%20Karma-orange)](https://mulearn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A modern, conversational web application built for the **MuLearn "Build a Simple Chatbot" Task (⭐ 250 Karma Points)**. Zenith AI combines Google's flagship **Gemini 2.5 Flash** generative model with a sleek **Streamlit** user interface, multi-persona adaptability, real-time response streaming, and an intelligent offline fallback engine.

---

## 🎯 Task Objective

Design and build a responsive, functional chatbot capable of holding natural, multi-turn conversations with users, complete with a modern web interface, local setup guide, and comprehensive technical documentation.

---

## 💡 What Makes Zenith AI Unique?

Unlike conventional single-purpose chatbots, **Zenith AI** delivers a flexible, robust conversational experience designed with students and developers in mind:

1. **🎭 Adaptive Multi-Persona System**:
   Switch effortlessly between 5 specialized personas via the sidebar:
   - 🎓 **Study & Tutor**: Explains intricate topics simply with analogies, step-by-step breakdowns, and comprehension checks.
   - 💻 **Code Mentor**: Senior software engineer persona that debugs errors, explains stack traces, and provides clean, commented code.
   - 🎭 **Creative & Humor**: Entertaining companion for clever jokes, tech puns, creative writing, and lighthearted conversation.
   - 🧘 **Mindfulness & Coach**: Empathetic listener offering stress-relief techniques, study-life balance advice, and affirmations.
   - ⚡ **General Assistant**: Fast, accurate, all-purpose assistant for summaries, drafting, and problem solving.

2. **⚡ Real-Time Response Streaming**:
   Utilizes the official `google-genai` SDK's `send_message_stream` coupled with Streamlit's `st.write_stream()` to deliver smooth, token-by-token animated text rendering.

3. **🛡️ Zero-Crash Hybrid Architecture (Intelligent Offline Fallback)**:
   If no API key is provided, or if network connectivity is interrupted, Zenith AI does not crash with an error. Instead, it seamlessly switches to an **Intelligent Offline Fallback Engine** that handles common queries, answers programming concepts, shares humor, and guides the user.

4. **🚀 One-Click Quick Starter Chips**:
   Context-sensitive sample prompt buttons appear on empty chats, enabling users and evaluators to test the chatbot immediately with a single click.

5. **📥 Session Export & Privacy**:
   Users can export their complete conversation history as structured JSON with one click. API keys entered in the sidebar reside strictly in memory within the current session.

---

## 🏗️ Technical Approach

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Frontend / Web UI** | [Streamlit](https://streamlit.io/) | Lightweight, responsive web interface with chat input, custom CSS styling, and sidebar controls |
| **Generative AI** | [Google Gemini 2.5 Flash](https://aistudio.google.com/) via `google-genai` | Multi-turn natural language understanding, reasoning, and real-time streaming |
| **Fallback Engine** | Rule-based Python Dispatcher | Local keyword heuristic matching for offline resilience |
| **State Management** | Streamlit Session State (`st.session_state`) | Multi-turn conversational memory preservation across reruns |

---

## 🚀 Getting Started (Run Locally)

Follow these steps to run Zenith AI on your local machine:

### 1. Prerequisites
- **Python 3.10** or higher installed ([Download Python](https://www.python.org/downloads/))
- Git installed on your system

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/zenith-ai-chatbot.git
cd zenith-ai-chatbot
```

### 3. Set Up a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Your Google Gemini API Key *(Optional)*
Zenith AI offers 3 flexible ways to supply an API key:

- **Method A (Easiest)**: Launch the app and enter your key in the sidebar text input field.
- **Method B (Streamlit Secrets)**:
  Copy the template file:
  ```bash
  cp .streamlit/secrets.toml.example .streamlit/secrets.toml
  ```
  Open `.streamlit/secrets.toml` and paste your key:
  ```toml
  GEMINI_API_KEY = "your_actual_gemini_api_key"
  ```
- **Method C (Environment Variable)**:
  ```bash
  # Windows PowerShell
  $env:GEMINI_API_KEY="your_actual_gemini_api_key"

  # Linux / macOS
  export GEMINI_API_KEY="your_actual_gemini_api_key"
  ```

> 🔑 Get a free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`** to interact with Zenith AI!

---

## 🌐 Deploy to Streamlit Community Cloud (Free Hosting)

To make your chatbot publicly accessible for anyone to try:

1. Push this repository to **GitHub**.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New App**, select your repository, branch (`main`), and set the main file path to `app.py`.
4. Click **Advanced settings...** -> **Secrets**, and add:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy!** Your chatbot will be live with a shareable URL (e.g. `https://zenith-chatbot.streamlit.app`).

---

## 🛠️ Challenges Faced & Solutions

### 1. Handling Missing API Keys Gracefully
* **Challenge**: When users or judges first clone the repository or open the web app without configuring an API key, standard API-dependent chatbots immediately crash with an unhandled exception (`KeyError` or authentication failure).
* **Solution**: Engineered an intelligent fallback layer in [`bot_engine.py`](file:///f:/Mulearn%20Task%20Files/chatbot/bot_engine.py). If no key is detected, the app automatically switches to **Demo / Offline Mode** with predefined knowledge, humor, and study tips, while alerting the user with an intuitive sidebar banner.

### 2. Maintaining Multi-Turn Context with Real-Time Streaming
* **Challenge**: Streaming token chunks in Streamlit often requires custom generators while maintaining the accumulated history for the GenAI chat model.
* **Solution**: Reconstructed previous conversation turns into Google GenAI's `types.Content` objects within `client.chats.create()`, and yielded `chunk.text` fragments directly through `st.write_stream()`, delivering a seamless token-by-token experience.

### 3. Dynamic Persona Transitioning
* **Challenge**: Switching between personas could contaminate conversation context if prompt rules were not re-applied dynamically.
* **Solution**: Decoupled persona configuration into [`personas.py`](file:///f:/Mulearn%20Task%20Files/chatbot/personas.py), ensuring that switching personas updates the active avatar, system instructions, and welcome cards in real time.

---

## 📸 Sample Conversation

```text
User: How do list comprehensions work in Python?

Zenith (💻 Code Mentor):
List comprehensions provide a concise way to create lists from existing iterables.

Instead of traditional loops:
  squares = []
  for x in range(5):
      squares.append(x**2)

You can write in one clean line:
  squares = [x**2 for x in range(5)]
  # Result: [0, 1, 4, 9, 16]

Syntax formula:
  [expression for item in iterable if condition]
```

---

## 📦 Deliverables Checklist

- [x] **Functional Chatbot**: Multi-turn conversation capability with persona customization.
- [x] **Web Interface**: Clean Streamlit UI with quick starter chips and session controls.
- [x] **Public GitHub Ready**: Git repository initialized with `.gitignore`, `requirements.txt`, and clean architecture.
- [x] **Documentation**: Complete setup, architecture explanation, creative process, and challenges.
- [x] **Deployment Ready**: Streamlit Community Cloud configuration and secrets management.

---

## 👤 Author & Acknowledgments

- **Developer**: Febin Jacob
- **Framework**: Streamlit & Google GenAI SDK
- **Community**: [µLearn Foundation](https://mulearn.org/)
