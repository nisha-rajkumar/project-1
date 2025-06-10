import streamlit as st
from fpdf import FPDF
import os
import google.generativeai as genai

# -------------------- Configuration --------------------
# Inbuilt Gemini API Key (ensure it's secure in real apps)
API_KEY = "AIzaSyC_iRD_Ss1ayBXadgIIrHAoMKu2xoXkTFY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# -------------------- Functions ------------------------

def build_prompt(text, format_, tone):
    return f"""
    Write an email based on the following input.
    Format: {format_}
    Tone: {tone}
    Content: {text}
    """

def generate_email(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating email: {e}"

def save_text_to_pdf(text, filename='generated_email.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename

# -------------------- Streamlit UI ---------------------

st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("📧 AI Email Generator using Gemini")

st.markdown("Fill in the details below to generate a professional email using AI.")

# --- User Input ---
user_input = st.text_area("✏️ Enter your message or key points for the email:", height=200)

# --- Format and Tone Selection ---
format_option = st.radio("📄 Select Email Format", ["Formal", "Informal", "Professional", "Friendly"], horizontal=True)
tone_option = st.selectbox("🎯 Select Tone", ["Polite", "Confident", "Apologetic", "Appreciative", "Neutral"])

# --- Generate Button ---
if st.button("🚀 Generate Email"):
    if user_input.strip():
        prompt = build_prompt(user_input, format_option, tone_option)
        email_output = generate_email(prompt)
        st.session_state['email_text'] = email_output
    else:
        st.warning("⚠️ Please enter the message or key points.")

# --- Regenerate Button ---
if st.button("🔁 Regenerate with New Format/Tone"):
    if user_input.strip():
        prompt = build_prompt(user_input, format_option, tone_option)
        email_output = generate_email(prompt)
        st.session_state['email_text'] = email_output
    else:
        st.warning("⚠️ Please enter the message or key points.")

# --- Display Output ---
if 'email_text' in st.session_state:
    st.subheader("📬 Generated Email")
    st.markdown(st.session_state['email_text'])

    # --- Download PDF Button ---
    pdf_file = save_text_to_pdf(st.session_state['email_text'])
    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download Email as PDF", f, file_name="generated_email.pdf", mime="application/pdf")

# Footer
st.markdown("---")
st.caption("Powered by Gemini AI | Streamlit App by OpenAI’s Assistant")
