# Spam Email Detection System 🛡️

**Live Application:** [View App Here](https://spam-email-detection-model-ezeon9yyfj7syxwetutxee.streamlit.app/)

## 📖 Overview
The **Spam Email Detection System** is an advanced AI tool designed to protect users from malicious emails, phishing attempts, and unsolicited spam. By utilizing state-of-the-art Natural Language Processing (NLP) techniques and Machine Learning algorithms, it provides real-time analysis of message content to ensure digital safety.

This project goes beyond simple keyword matching, employing an intelligent model that understands linguistic patterns and potential threats.

## 🚀 Key Features
- **Machine Learning Analysis**: Uses a Logistic Regression model with TF-IDF Vectorization for high-accuracy classification.
- **NLP Preprocessing**: Automatically cleans text, removes punctuation, and filters stopwords for better pattern recognition.
- **Real-Time Threat Detection**: Instant analysis of pasted email content with specialized risk factor identification.
- **Modern AI Dashboard**: A professional, dark-themed interface built for clarity and efficiency.

## 🛠️ Technical Stack
- **Languages**: Python
- **Framework**: Streamlit (Frontend)
- **Natural Language Processing**: NLTK (Natural Language Toolkit)
- **Data Science**: Pandas, Scikit-Learn (TF-IDF, Logistic Regression)

## 🛡️ Security Analysis
The system evaluates multiple security vectors:
- **Urgency & Pressure**: Detects high-pressure tactics commonly used in phishing.
- **Suspicious Links**: Identifies potential malicious URLs.
- **Credential Requests**: Flags attempts to solicit passwords or sensitive info.
- **Formatting Anomalies**: Analyzes capitalization and punctuation patterns.

## 🚀 Installation & Running Locally
1. Clone the repository:
   ```bash
   git init
   git remote add origin https://github.com/yvsns-hub/SPAM-EMAIL-DETECTION-MODEL.git
   git pull origin main
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 📜 License
This project is licensed under the MIT License.
