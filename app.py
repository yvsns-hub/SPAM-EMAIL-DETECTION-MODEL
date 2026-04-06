import streamlit as st
import pandas as pd
import pickle
import string
import nltk
from nltk.corpus import stopwords

# Page configuration
st.set_page_config(
    page_title="Spam Email Detection System",
    page_icon="🛡️",
    layout="centered"
)

# Download NLTK data
nltk.download('stopwords')

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextArea>div>div>textarea {
        background-color: white;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 1.5rem;
        font-weight: bold;
    }
    .spam { background-color: #ffcccc; color: #cc0000; border: 1px solid #cc0000; }
    .ham { background-color: #ccffcc; color: #006600; border: 1px solid #006600; }
</style>
""", unsafe_allow_html=True)

# Load model and vectorizer
try:
    with open('spam_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf = pickle.load(f)
except FileNotFoundError:
    st.error("Model or Vectorizer file not found. Please run 'train.py' first.")
    st.stop()

def transform_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)

# Header
st.title("🛡️ Spam Email Detection System")
st.write("Analyze emails to identify potential threats and spam content.")
st.markdown("---")

# Input
input_sms = st.text_area("Paste the email or message content here", height=200)

if st.button("🔍 Analyze Message"):
    if input_sms.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        # Preprocess
        transformed_sms = transform_text(input_sms)
        
        # Vectorize
        vector_input = tfidf.transform([transformed_sms])
        
        # Predict
        # Label mapping: spam -> 0, ham -> 1 (as per original notebook)
        result = model.predict(vector_input)[0]
        
        # Display
        if result == 0:
            st.markdown('<div class="result-box spam">🚨 SPAM DETECTED! This message might be dangerous.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box ham">✅ HAM! This message appears to be safe and legitimate.</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Machine Learning powered security for your inbox.")
