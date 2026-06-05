# day2_production.py — Word Blitz Production Validator v2
import google.generativeai as genai
from dotenv import load_dotenv
import os, json
from dataclasses import dataclass

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ─────────────────────────────────────────────
# This is your Day 1 validator. It was naive.
# It would reject "Aam" for Fruits because no examples.
# It had no structured output — you were doing string matching.
# Day 2 fixes both.
# ─────────────────────────────────────────────

VALIDATOR_SYSTEM_V2 = """You are the answer validator for Word Blitz — a real-time multilingual word game.
Players answer in English, Hindi, or Punjabi. All three are valid.

RULES:
1. Accept words in English, Hindi (Devanagari or romanized), or Punjabi (Gurmukhi or romanized)
2. Proper nouns count IF they are genuinely in the category (Shera = animal name = CORRECT for Animals)
3. Slang counts if widely understood
4. Spelling variations count (colour/color, aam/aama both valid for mango)

EXAMPLES (few-shot):
Category: Animals | Word: Tiger → CORRECT (English)
Category: Animals | Word: Haathi → CORRECT (Hindi for elephant)
Category: Animals | Word: Sher → CORRECT (Hindi/Punjabi for lion)
Category: Animals | Word: Mango → WRONG (it's a fruit, not an animal)
Category: Fruits | Word: Aam → CORRECT (Hindi for mango)
Category: Fruits | Word: Kela → CORRECT (Hindi for banana)
Category: Fruits | Word: Table → WRONG (not a fruit in any language)
Category: Colors | Word: Laal → CORRECT (Hindi/Punjabi for red)
Category: Colors | Word: Neela → CORRECT (Hindi for blue)

THINK BEFORE YOU ANSWER:
- What language is this word in?
- What does it mean?
- Does the meaning belong to the category?

RESPOND WITH ONLY RAW JSON — no markdown, no explanation outside JSON:
{
  "verdict": "CORRECT" or "WRONG",
  "language": "English" | "Hindi" | "Punjabi" | "Other",
  "confidence": 0.0 to 1.0,
  "word_meaning": "what the word means in English",
  "reason": "one sentence"
}"""

@dataclass
class ValidationResult:
    verdict: str
    language: str
    confidence: float
    word_meaning: str
    reason: str
    raw_response: str  # always keep raw — for debugging

def validate_answer(category: str, word: str) -> ValidationResult:
    model = genai.GenerativeModel(
        "gemini-2.5-flash-lite",
        system_instruction=VALIDATOR_SYSTEM_V2
    )
    
    user_message = f"Category: {category} | Word: {word}"
    
    response = model.generate_content(
        user_message,
        generation_config=genai.GenerationConfig(
            temperature=0.1,      # consistency for validation
            max_output_tokens=150  # JSON response is small, cap tightly
        )
    )
    
    raw = response.text.strip()
    
    # Strip markdown code fences if model adds them (it sometimes does)
    # This is the real-world fix — models aren't always perfectly obedient
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    try:
        data = json.loads(raw)
        return ValidationResult(
            verdict=data["verdict"],
            language=data["language"],
            confidence=data["confidence"],
            word_meaning=data["word_meaning"],
            reason=data["reason"],
            raw_response=raw
        )
    except (json.JSONDecodeError, KeyError) as e:
        # Graceful degradation — never crash in production
        # Log the error, return a safe default
        print(f"⚠️ Parse error: {e}\nRaw: {raw}")
        return ValidationResult(
            verdict="WRONG",
            language="Unknown",
            confidence=0.0,
            word_meaning="parse error",
            reason="Validation service error",
            raw_response=raw
        )

# Test it
if __name__ == "__main__":
    test_cases = [
        ("Animals", "Haathi"),
        ("Fruits", "Aam"),
        ("Colors", "Laal"),
        ("Animals", "Table"),
        ("Vegetables", "Gobhi"),
        ("Animals", "Sher"),
    ]
    
    print("Word Blitz Validator v2 — Production Grade\n" + "="*45)
    for category, word in test_cases:
        result = validate_answer(category, word)
        status = "✅" if result.verdict == "CORRECT" else "❌"
        print(f"{status} [{category}] '{word}' ({result.language}) → {result.verdict}")
        print(f"   Means: {result.word_meaning} | Confidence: {result.confidence}")
        print(f"   Reason: {result.reason}\n")