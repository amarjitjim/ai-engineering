from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()
# --- CONFIGURATION ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # paste your key here
model=genai.GenerativeModel("gemini-2.5-flash-lite")

def ask(system:str,user:str,temp:float=0.1)->str:
    m =genai.GenerativeModel("gemini-2.5-flash-lite",
                            system_instruction=system
                            )
    r=m.generate_content(user,generation_config=genai.GenerationConfig(
        temperature=temp,
        max_output_tokens=300
    ))

    return r.text.strip()


# ─────────────────────────────────────────────
# TECHNIQUE 1: ZERO-SHOT
# No examples. Just instructions. Works for simple tasks.
# ─────────────────────────────────────────────
zero_shot_system = """You are a sentiment classifier.
Classify the sentiment of the given text as: POSITIVE, NEGATIVE, or NEUTRAL.
Reply with only the label."""

print("=== ZERO-SHOT ===")
print(ask(zero_shot_system, "The game was so much fun, I played for 3 hours!"))
print(ask(zero_shot_system, "I waited 45 minutes and nobody helped me."))
print(ask(zero_shot_system, "The package arrived on Tuesday."))

# ─────────────────────────────────────────────
# TECHNIQUE 2: FEW-SHOT
# Show examples IN the system prompt. Model pattern-matches.
# Use when zero-shot gives inconsistent or wrong format output.
# ─────────────────────────────────────────────
few_shot_system = """You are a Word Blitz answer validator.
A player gives a word. You decide if it belongs to the category.

Examples:
Category: Animals | Word: Tiger → CORRECT
Category: Animals | Word: Mango → WRONG
Category: Animals | Word: Shera → CORRECT  ← proper noun animal name counts
Category: Fruits   | Word: Kela → CORRECT  ← Hindi word counts
Category: Fruits   | Word: Chair → WRONG

Reply with ONLY: CORRECT or WRONG"""

print("\n=== FEW-SHOT (Word Blitz) ===")
print(ask(few_shot_system, "Category: Animals | Word: Haathi"))   # Hindi for elephant
print(ask(few_shot_system, "Category: Fruits | Word: Aam"))       # Hindi for mango
print(ask(few_shot_system, "Category: Animals | Word: Table"))

# ─────────────────────────────────────────────
# TECHNIQUE 3: CHAIN-OF-THOUGHT
# Tell the model to reason BEFORE answering.
# Critical for anything involving logic, math, or edge cases.
# ─────────────────────────────────────────────
cot_system = """You are a Word Blitz validator for a multilingual game.

Before giving your verdict, think through:
1. What language is this word in? (English, Hindi, Punjabi, or other)
2. What does it mean?
3. Does it belong to the category?

Format your response EXACTLY like this:
Thinking: [your reasoning]
Verdict: CORRECT or WRONG"""

print("\n=== CHAIN-OF-THOUGHT ===")
print(ask(cot_system, "Category: Vegetables | Word: Gobhi"))  # Cauliflower in Hindi/Punjabi

# ─────────────────────────────────────────────
# TECHNIQUE 4: STRUCTURED OUTPUT
# Force JSON. Parse it in code. Never do string matching on AI output.
# This is what separates toy projects from production systems.
# ─────────────────────────────────────────────
structured_system = """You are a Word Blitz validator.

Respond ONLY with a JSON object. No explanation. No markdown. Just raw JSON.

{
  "verdict": "CORRECT" or "WRONG",
  "language": "English" | "Hindi" | "Punjabi" | "Other",
  "confidence": 0.0 to 1.0,
  "reason": "one sentence explanation"
}"""

import json

print("\n=== STRUCTURED OUTPUT ===")
raw = ask(structured_system, "Category: Colors | Word: Laal")  # Red in Hindi
print("Raw response:", raw)
try:
    parsed = json.loads(raw)
    print(f"Verdict: {parsed['verdict']}")
    print(f"Language: {parsed['language']}")
    print(f"Confidence: {parsed['confidence']}")
    print(f"Reason: {parsed['reason']}")
except json.JSONDecodeError:
    print("⚠️ Model didn't return clean JSON — we'll fix this in Day 27 with instructor library")