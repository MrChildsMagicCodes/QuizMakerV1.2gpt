import openai
import os
import json

# Set OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_questions_with_gpt(text):
    prompt = f"""
You are a tool that extracts multiple-choice quiz questions from plain text and outputs them in strict JSON format.

Each question must include:
- "question": the question text
- "choices": a list of 3–5 answer options
- "answer": the letter of the correct choice (e.g., "A", "B")

Rules:
- Output only valid JSON (no markdown, no explanation)
- Do not wrap the JSON in triple backticks
- Do not include any text before or after the JSON list

Example output:
[
  {{
    "question": "What is the capital of France?",
    "choices": ["Berlin", "Madrid", "Paris", "Rome"],
    "answer": "C"
  }},
  {{
    "question": "Which gas do plants use for photosynthesis?",
    "choices": ["Oxygen", "Carbon Dioxide", "Hydrogen", "Nitrogen"],
    "answer": "B"
  }}
]

Now extract the questions from this text:

{text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a quiz extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        content = response.choices[0].message["content"]
        return json.loads(content)
    except Exception as e:
        print("GPT error:", e)
        return []
