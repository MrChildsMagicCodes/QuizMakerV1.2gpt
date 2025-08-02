import streamlit as st
from PIL import Image
import pytesseract
from utils.gpt_parser import extract_questions_with_gpt
from utils.qti_builder import build_qti_zip
import base64
import tempfile
import os

st.set_page_config(page_title="🧙‍♂️ Magical Canvas Quiz Maker", layout="wide")

# Magic styling with banner
st.markdown("""
    <style>
    .magical-box {
        border: 5px double #8e44ad;
        padding: 1.5rem;
        background: #fefae0;
        border-radius: 20px;
        box-shadow: 0 0 15px #9c27b0;
        margin-top: 20px;
    }
    .magical-title {
        color: #6a1b9a;
        text-shadow: 1px 1px 2px #ce93d8;
        font-size: 32px;
    }
    .banner {
        background: linear-gradient(to right, #6a1b9a, #8e44ad);
        color: white;
        padding: 1rem;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 2rem;
        font-size: 36px;
        font-weight: bold;
        text-shadow: 1px 1px 2px black;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="banner">🧙‍♂️ Mr. Childs Magical Quiz Maker</div>', unsafe_allow_html=True)
st.markdown('<div class="magical-box">Upload a screenshot of quiz questions and generate a Canvas-ready QTI file using GPT magic!</div>', unsafe_allow_html=True)

# API Key input
api_key = st.text_input("🔑 Enter your OpenAI API key to activate GPT parsing", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# Upload image
uploaded_image = st.file_uploader("📤 Upload Screenshot", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR step
    with st.spinner("🔍 Extracting text with OCR..."):
        extracted_text = pytesseract.image_to_string(image)

    st.text_area("📜 Extracted Text", value=extracted_text, height=200)

    # GPT Parsing
    if st.button("🧠 Cast GPT Spell to Extract Questions"):
        if not api_key:
            st.error("🛑 You must enter a valid OpenAI API key to use GPT.")
        else:
            with st.spinner("✨ Summoning GPT..."):
                questions = extract_questions_with_gpt(extracted_text)
                if not questions:
                    st.error("🧟‍♂️ The spell failed. No questions extracted.")
                else:
                    st.session_state["questions"] = questions

# Question Review
if "questions" in st.session_state and st.session_state["questions"]:
    st.markdown('<h2 class="magical-title">🔮 Review Extracted Questions</h2>', unsafe_allow_html=True)
    for i, q in enumerate(st.session_state["questions"], 1):
        st.markdown(f"**Q{i}: {q['question']}**")
        for j, choice in enumerate(q['choices']):
            prefix = chr(65 + j)
            st.markdown(f"- {prefix}. {choice}")
        st.markdown(f"✅ Correct Answer: **{q['answer']}**")
        st.markdown("---")

    # Export button
    if st.button("📦 Create QTI ZIP Scroll"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            build_qti_zip(st.session_state["questions"], tmp.name)
            with open(tmp.name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/zip;base64,{b64}" download="canvas_quiz.zip">📥 Download Enchanted QTI Zip</a>'
                st.markdown(href, unsafe_allow_html=True)
