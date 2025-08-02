# Canvas Quiz Generator from Screenshots (with ChatGPT)

This app lets you paste quiz screenshots, uses GPT to extract multiple-choice questions, and generates a Canvas-ready QTI `.zip` file.

## 🔧 Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🧠 GPT API Key

Set your OpenAI API key via environment variable or in Streamlit Cloud:

```
OPENAI_API_KEY=your-key-here
```

## 📦 Output

Click "Download QTI ZIP" to get a Canvas-importable quiz.

Use "Import Course Content" → "QTI .zip File" in Canvas to upload.
