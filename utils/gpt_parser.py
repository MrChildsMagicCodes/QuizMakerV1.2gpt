import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_questions_with_gpt(text):
    prompt = f"Extract multiple choice questions from the following text. Format each question as a JSON object with keys: 'question', 'choices' (list of strings), and 'answer' (e.g., 'A').\n\n{text}\n\nOutput:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a quiz parser."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        content = response.choices[0].message["content"]
        return eval(content) if content.startswith("[") else []
    except Exception as e:
        print("GPT error:", e)
        return []
