import streamlit as st
import pandas as pd
import pickle
import string
import nltk
from datetime import datetime
from nltk.corpus import stopwords

# Page configuration
st.set_page_config(
    page_title="🛡️ AI Suite | Spam Detection",
    page_icon="🛡️",
    layout="wide"
)

# Download NLTK data
nltk.download('stopwords')

# Custom CSS for professional technical theme (Restoring the EXACT "AI Suite" experience)
st.markdown("""
<style>
    :root {
        --primary-color: #0f172a;
        --secondary-color: #1e293b;
        --accent-color: #0ea5e9;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --border-color: #334155;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 100%);
        color: #e2e8f0;
    }
    
    .header-container {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.2);
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ef4444;
        padding: 1rem 0;
        border-bottom: 2px solid #ef4444;
        margin: 1.5rem 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .result-safe {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 2px solid #10b981;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .result-spam {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 2px solid #ef4444;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .risk-meter {
        width: 100%;
        height: 12px;
        background: #334155;
        border-radius: 6px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .risk-meter-fill {
        height: 100%;
        background: linear-gradient(90deg, #10b981, #ef4444);
        transition: width 0.5s ease;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Load model and vectorizer
try:
    with open('spam_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf = pickle.load(f)
except FileNotFoundError:
    st.error("Model files not found. Please run 'train.py' first.")
    st.stop()

def transform_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    return ' '.join([word for word in tokens if word not in stop_words])

# Header
st.markdown("""
    <div class="header-container">
        <h1>🛡️ AI Suite | Spam Detection</h1>
        <p>Enterprise-grade security engine for real-time automatic spam and phishing threat detection.</p>
    </div>
""", unsafe_allow_html=True)

# Main Form
with st.container():
    st.markdown('<div class="section-header">📧 Email Content</div>', unsafe_allow_html=True)
    email_body = st.text_area("Paste Email Content Here", height=250, placeholder="Paste the complete email content (subject + body) here for automatic analysis...", help="The system will automatically detect all characteristics from the email content")
    
    if st.button("🔍 ANALYZE EMAIL"):
        if not email_body.strip():
            st.error("⚠️ Please paste email content to analyze")
        else:
            # RESTORING FULL HEURISTIC SCORING ENGINE FROM ORIGINAL app.py
            email_lower = email_body.lower()
            spam_score = 0
            spam_factors = []
            
            # 1. Check for hyperlinks
            if 'http://' in email_lower or 'https://' in email_lower or 'www.' in email_lower:
                spam_score += 15
                spam_factors.append("Contains hyperlinks/URLs")
            
            # 2. Check for attachment references
            if any(k in email_lower for k in ['attachment', 'file', 'download', 'open attached', 'see attached']):
                spam_score += 10
                spam_factors.append("References attachments or files")
            
            # 3. Detect urgency/pressure tactics
            critical_urgency = ['urgent', '!!', 'immediately', 'asap', 'act now', 'do not delay']
            high_urgency = ['important', 'time sensitive', 'limited time', 'hurry', 'today', 'now']
            if any(w in email_lower for w in critical_urgency):
                spam_score += 25
                spam_factors.append("Critical urgency/pressure tactics detected")
            elif any(w in email_lower for w in high_urgency):
                spam_score += 15
                spam_factors.append("High urgency/pressure tactics detected")
            
            # 4. Check for credential requests
            credential_keywords = ['verify', 'confirm', 'login', 'password', 'username', 'account', 'update information', 'reactivate', 'validate']
            credential_patterns = sum(1 for keyword in credential_keywords if keyword in email_lower)
            if credential_patterns >= 2:
                spam_score += 40
                spam_factors.append("Requests credentials/sensitive information (HIGH RISK)")
            elif credential_patterns == 1:
                spam_score += 20
                spam_factors.append("Potential credential request")
            
            # 5. Suspicious domains/spoofing
            if any(k in email_lower for k in ['paypal', 'amazon', 'apple', 'microsoft', 'bank', 'verify your account']):
                spam_score += 30
                spam_factors.append("Potential domain spoofing/impersonation detected")
            
            # 6. Formatting anomalies
            excess_caps = sum(1 for char in email_body if char.isupper()) / max(len(email_body), 1)
            if excess_caps > 0.4:
                spam_score += 12
                spam_factors.append("Excessive capitalization detected")
            
            excess_punctuation = email_body.count('!') + email_body.count('?') * 0.5
            if excess_punctuation > 5:
                spam_score += 8
                spam_factors.append("Excessive punctuation detected")
            
            # 7. Spam keywords
            spam_keywords = ['click here', 'congratulations', 'claim reward', 'free money', 'winner', 'inherited']
            keyword_count = sum(1 for k in spam_keywords if k in email_lower)
            spam_score += (keyword_count * 8)
            if keyword_count > 0:
                spam_factors.append(f"Detected {keyword_count} common spam keyword(s)")
            
            # 8. Repetitive content
            words = email_lower.split()
            if words:
                word_freq = {w: words.count(w) for w in set(words)}
                if max(word_freq.values()) > len(words) * 0.2:
                    spam_score += 10
                    spam_factors.append("Repetitive content pattern detected")
            
            # ML MODEL AS SECOND OPINION
            transformed_sms = transform_text(email_body)
            vector_input = tfidf.transform([transformed_sms])
            ml_prediction = model.predict(vector_input)[0]  # 0: Spam, 1: Ham
            if ml_prediction == 0:
                spam_score = max(spam_score, 65) # Ensure it's in the SPAM range
            
            # Cap at 100
            spam_score = min(spam_score, 100)
            
            # Classification
            if spam_score < 30:
                classification = "SAFE"
                confidence = 95 - (spam_score / 2)
            elif spam_score < 60:
                classification = "SUSPICIOUS"
                confidence = 85 - (spam_score / 3)
            else:
                classification = "SPAM/PHISHING"
                confidence = 90 + (spam_score / 10)
            
            # Display Results
            st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
            
            if classification == "SAFE":
                st.markdown(f"""
                    <div class="result-safe">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #10b981; margin-bottom: 0.5rem;">✅ SAFE</div>
                        <p>This email appears to be legitimate and safe.</p>
                        <div class="risk-meter"><div class="risk-meter-fill" style="width: {spam_score}%; background: #10b981;"></div></div>
                        <p>Spam Score: <strong>{spam_score}/100</strong> | Confidence: <strong>{confidence:.1f}%</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            elif classification == "SUSPICIOUS":
                st.markdown(f"""
                    <div class="result-spam">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b; margin-bottom: 0.5rem;">⚠️ SUSPICIOUS</div>
                        <p>This email shows some characteristics of spam or phishing. Exercise caution.</p>
                        <div class="risk-meter"><div class="risk-meter-fill" style="width: {spam_score}%; background: #f59e0b;"></div></div>
                        <p>Spam Score: <strong>{spam_score}/100</strong> | Confidence: <strong>{confidence:.1f}%</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="result-spam">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #ef4444; margin-bottom: 0.5rem;">🚨 SPAM/PHISHING DETECTED</div>
                        <p>This email is likely spam or a phishing attempt. <strong>Do not click links or open attachments.</strong></p>
                        <div class="risk-meter"><div class="risk-meter-fill" style="width: {spam_score}%;"></div></div>
                        <p>Spam Score: <strong>{spam_score}/100</strong> | Confidence: <strong>{confidence:.1f}%</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            
            if spam_factors:
                st.markdown('<div class="section-header">⚠️ Detected Risk Factors</div>', unsafe_allow_html=True)
                for i, factor in enumerate(spam_factors, 1):
                    st.markdown(f"- **{i}.** {factor}")

st.markdown("---")
st.caption("© 2024 AI Suite Professional Security Solutions. Powered by Hybrid Multi-Vector Analysis.")
