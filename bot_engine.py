"""
Chat engine module for Zenith AI.
Handles Gemini API client setup, multi-turn chat streaming,
and intelligent offline fallback when API keys are not supplied.
"""

import time
import os
import random
from typing import Generator, List, Dict, Any, Optional

# Attempt to import google-genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
    types = None


# Pre-packaged responses for offline / demo mode
OFFLINE_KNOWLEDGE = {
    "greetings": [
        "Hello there! I'm **Zenith AI**. How can I help you learn, code, or brainstorm today?",
        "Greetings! Zenith is ready to assist. What's on your mind?",
        "Hi! Great to chat with you. Feel free to ask me anything or try one of the quick starters above!"
    ],
    "jokes": [
        "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
        "There are 10 types of people in the world: those who understand binary, and those who don't. 😄",
        "A SQL query walks into a bar, walks up to two tables and asks: *'Can I join you?'* 🍻",
        "Why do Java programmers wear glasses?\nBecause they don't C#! 👓",
        "How many programmers does it take to change a lightbulb?\nNone, that's a hardware problem! 💡"
    ],
    "python": [
        "Python is one of the most versatile languages in the world! Key highlights:\n\n"
        "- **Simple & Readable**: Reads almost like plain English.\n"
        "- **Dynamic Typing**: No need to declare variable types explicitly.\n"
        "- **Batteries Included**: Vast standard library and ecosystem (NumPy, Pandas, Streamlit, PyTorch).\n\n"
        "```python\n# Classic Python greeting\ndef greet(name: str) -> str:\n    return f'Hello, {name}! Welcome to Python.'\n\nprint(greet('Explorer'))\n```",
        "Here's a quick Python tip on list comprehensions:\n\n"
        "Instead of:\n```python\nsquares = []\nfor x in range(10):\n    squares.append(x**2)\n```\n\n"
        "You can write cleanly:\n```python\nsquares = [x**2 for x in range(10)]\n```"
    ],
    "study": [
        "Here are 3 high-impact study techniques backed by cognitive science:\n\n"
        "1. **Active Recall**: Test yourself frequently rather than passively re-reading notes.\n"
        "2. **Spaced Repetition**: Review concepts over increasing intervals (Day 1, Day 3, Day 7, Day 14).\n"
        "3. **Feynman Technique**: Explain the topic simply in your own words as if teaching a beginner.",
        "To beat procrastination:\n\n"
        "- Use the **2-Minute Rule**: If a task takes under 2 minutes, do it right now.\n"
        "- Try the **Pomodoro Technique**: 25 minutes of laser-focused work followed by a 5-minute break."
    ],
    "mindfulness": [
        "Take a slow, deep breath in through your nose for 4 seconds... hold for 4 seconds... and gently exhale for 6 seconds. 🧘\n\n"
        "Remember: You don't have to figure everything out today. Progress is built one step at a time.",
        "Pause for a moment and celebrate how far you've come. Every expert was once a beginner."
    ],
    "default": [
        "I received your message! Currently running in **Demo / Offline Mode**.\n\n"
        "To unlock full Generative AI capabilities powered by Google Gemini:\n"
        "1. Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).\n"
        "2. Enter it in the sidebar on the left.\n"
        "3. Ask any complex question, debug code, or brainstorm ideas!\n\n"
        "In the meantime, feel free to ask about Python, coding tips, study strategies, or tell me to tell you a joke!"
    ]
}


def get_offline_response(prompt: str, persona_name: str) -> Generator[str, None, None]:
    """Generates an intelligent simulated streaming response when offline."""
    lower_prompt = prompt.lower().strip()
    
    if any(k in lower_prompt for k in ["hi", "hello", "hey", "greet", "who are you", "what are you"]):
        response = random.choice(OFFLINE_KNOWLEDGE["greetings"])
    elif any(k in lower_prompt for k in ["joke", "funny", "laugh", "humor", "pun"]):
        response = random.choice(OFFLINE_KNOWLEDGE["jokes"])
    elif any(k in lower_prompt for k in ["python", "code", "programming", "bug", "debug", "function"]):
        response = random.choice(OFFLINE_KNOWLEDGE["python"])
    elif any(k in lower_prompt for k in ["study", "exam", "learn", "technique", "procrastinat"]):
        response = random.choice(OFFLINE_KNOWLEDGE["study"])
    elif any(k in lower_prompt for k in ["calm", "stress", "breath", "mindful", "relax", "burnout"]):
        response = random.choice(OFFLINE_KNOWLEDGE["mindfulness"])
    else:
        response = random.choice(OFFLINE_KNOWLEDGE["default"])

    # Simulate realistic token streaming with slight delay
    words = response.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.02)


def stream_gemini_chat(
    api_key: str,
    messages: List[Dict[str, str]],
    user_prompt: str,
    system_instruction: str,
    model_name: str = "gemini-2.5-flash",
    temperature: float = 0.7
) -> Generator[str, None, None]:
    """
    Connects to the Google GenAI SDK and streams responses for multi-turn chats.
    Falls back gracefully if an error occurs.
    """
    if not GENAI_AVAILABLE:
        yield "⚠️ `google-genai` library is not installed. Please run `pip install google-genai`.\n\n"
        yield from get_offline_response(user_prompt, "Offline")
        return

    try:
        client = genai.Client(api_key=api_key)

        # Build conversation history in google-genai types format
        history_contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            history_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        # Configure chat generation parameters
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature
        )

        chat = client.chats.create(
            model=model_name,
            config=config,
            history=history_contents
        )

        response_stream = chat.send_message_stream(user_prompt)
        has_content = False

        for chunk in response_stream:
            if chunk.text:
                has_content = True
                yield chunk.text

        if not has_content:
            yield "*(No response generated by model. Please check the prompt or try again.)*"

    except Exception as exc:
        error_msg = str(exc)
        yield f"⚠️ **Gemini API Notice**: {error_msg}\n\n"
        yield "Switching to fallback offline response:\n\n"
        yield from get_offline_response(user_prompt, "Fallback")
