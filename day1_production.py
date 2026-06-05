# day1_production.py
# This pattern is what you'll use in EVERY real project

from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()
# --- CONFIGURATION ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # paste your key here

# --- SYSTEM PROMPT AS A VARIABLE (not hardcoded in the call) ---
# Why? Because in production you swap this per client, per use case
# Word Blitz will have a different system prompt than a PDF chatbot

WORD_BLITZ_SYSTEM_PROMPT="""
You are the judge for Word Blitz, a multilingual vocabulary game.
The player is given a word and must define it correctly.

Rules:
- Accept answers in English, Hindi, or Punjabi
- Be lenient with synonyms — if the meaning is correct, accept it
- Respond ONLY with: CORRECT or INCORRECT, then one line of explanation
- Never give the full definition before the player answers
"""

model=genai.GenerativeModel(model_name="gemini-2.5-flash-lite",system_instruction=WORD_BLITZ_SYSTEM_PROMPT)

# Simulate a player answering
player_word = "ephemeral"
player_answer = "something that doesn't last long"

# The user message is dynamic — changes every call
user_message = f'Word: "{player_word}"\nPlayer answer: "{player_answer}"'

response=model.generate_content(user_message,generation_config=genai.GenerationConfig(temperature=0.1,max_output_tokens=1000))
print(response.text)
print(f"\n Token used:{response.usage_metadata.total_token_count}")