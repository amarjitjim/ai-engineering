# AI Engineering — 90 Days
 
Learning journey from React Native + Python developer to AI Engineer.
Building real projects. Shipping every session.
 
**Goal:** Remote AI job + Upwork/Toptal contracts in 90 days.  
**Stack:** Python, Gemini API (free tier), LangChain, ChromaDB, FastAPI, React Native  
**Real project:** [Word Blitz](https://github.com/amarjitjim/ai-engineering) — voice-based multilingual AI game (English, Hindi, Punjabi)
 
---
 
## Progress
 
| Day | Topic | Status | Files |
|-----|-------|--------|-------|
| 1 | LLM API Basics — tokens, context window, temperature, system vs user prompts | ✅ | `day1_basic.py`, `day1_production.py` |
| 2 | Prompt Engineering — zero-shot, few-shot, chain-of-thought, structured output | ✅ | `day2_prompts.py`, `day2_production.py` |
| 3 | Streaming Responses | ⏳ | — |
| 4 | Embeddings | ⏳ | — |
| 5 | Build #1 — CLI Chatbot with Memory | ⏳ | — |
| 6 | Vector Databases — ChromaDB | ⏳ | — |
| 7 | Document Chunking | ⏳ | — |
| 8 | Build #2 — PDF Q&A Bot | ⏳ | — |
| 9 | RAG Evaluation | ⏳ | — |
| 10 | RAG vs Fine-tuning | ⏳ | — |
 
---
 
## What's Been Built
 
### Day 1 — Word Blitz Answer Validator v1
**File:** `day1_production.py`  
Basic answer validator for Word Blitz game. Validates if a player's word belongs to a given category.
 
**Concepts applied:**
- Gemini 2.5 Flash API (free tier)
- System prompt vs user prompt separation
- Token tracking with `usage_metadata`
- `temperature=0.1` for consistent validation output
- `.env` + `python-dotenv` for API key management
---
 
### Day 2 — Word Blitz Answer Validator v2 (Production Grade)
**File:** `day2_production.py`  
Upgraded validator with multilingual support (English, Hindi, Punjabi), structured JSON output, and graceful error handling.
 
**Concepts applied:**
- **Zero-shot** — instructions only, no examples
- **Few-shot** — Hindi/Punjabi word examples in system prompt (Aam, Kela, Haathi, Laal)
- **Chain-of-thought** — model reasons before answering
- **Structured output** — returns validated JSON with verdict, language, confidence, meaning
- **Defensive parsing** — regex JSON extraction handles model non-compliance
- **Input validation** — filters nonsense input before the API call (saves tokens)
**Sample output:**
```
✅ [Animals] 'Haathi' (Hindi) → CORRECT | Means: Elephant | Confidence: 1.0
✅ [Fruits]  'Aam'    (Hindi) → CORRECT | Means: Mango    | Confidence: 1.0
✅ [Colors]  'Laal'   (Hindi) → CORRECT | Means: Red      | Confidence: 1.0
❌ [Animals] 'Table'  (English) → WRONG | Means: Furniture | Confidence: 1.0
```
 
**File:** `day2_prompts.py`  
All four prompt engineering techniques demonstrated side by side.
 
---
 
## Key Concepts Learned
 
### Tokens
Unit of billing. ~¾ of a word. Always track with `usage_metadata`. Always set `max_output_tokens`.
 
### Context Window
Stateless — like a React component with no state. Every API call starts fresh. Everything must be passed every time.
 
### Temperature
Creativity dial. `0.0` = deterministic. `1.0` = creative but unpredictable. Use `0.1` for validation tasks.
 
### Prompt Engineering
- **Zero-shot:** Instructions only. Works for simple tasks.
- **Few-shot:** Show examples. Model pattern-matches. Essential for multilingual/edge cases.
- **Chain-of-thought:** Tell model to reason first. Doubles quality on complex inputs.
- **Structured output:** Force JSON. Parse it in code. Never string-match on AI output.
### Production Habits
- Never hardcode API keys — always `.env` + `os.getenv()`
- System prompt and user message always structurally separate
- Fix at two layers: prompt prevention + defensive parsing
- Filter invalid input in Python before the API call — LLMs are expensive, `if` statements are free
- Negative instructions matter as much as positive ones
---
 
## Setup
 
```bash
git clone https://github.com/amarjitjim/ai-engineering
cd ai-engineering
pip install google-generativeai python-dotenv
```
 
Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```
 
Get a free API key at: https://aistudio.google.com/app/apikey
 
Run any file:
```bash
python day1_basic.py
python day1_production.py
python day2_prompts.py
python day2_production.py
```
 
---
 
## About
 
Built by Amarjit — React Native + Python developer from Patiala, Punjab.  
Currently building: Word Blitz — voice-based multilingual AI game.
 


