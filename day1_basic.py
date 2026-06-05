# day1_basics.py
# pip install google-generativeai

import google.generativeai as genai

# --- CONFIGURATION ---
genai.configure(api_key="AIzaSyBZvjKdIDvC92Awqu73_zNmKEyDUtfYCAE")  # paste your key here

# --- THE MODEL ---
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",   # fast + free tier friendly

    # THIS is the system prompt — sets the personality for ALL messages
    # Think of it as your component's default props
    system_instruction="You are a helpful tutor for Indian students. "
                       "Always explain with simple Indian English. "
                       "Give one real-life example from daily life in India."
)

# --- SINGLE API CALL ---
response = model.generate_content(
    "Explain what machine learning is in 3 sentences.",

    generation_config=genai.GenerationConfig(
        temperature=0.3,      # mostly focused, little creativity
        max_output_tokens=200 # hard cap — controls cost
    )
)

print(response.text)

# --- LOOK AT TOKEN USAGE (THIS IS YOUR BILLING METER) ---
print("\n--- Token Usage ---")
print(f"Input tokens:  {response.usage_metadata.prompt_token_count}")
print(f"Output tokens: {response.usage_metadata.candidates_token_count}")
print(f"Total tokens:  {response.usage_metadata.total_token_count}")