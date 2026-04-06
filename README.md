# Spam Email Detection System 🛡️

Detect spam and phishing attempts using Machine Learning.

## Features
- Real-time Spam/Ham classification
- NLTK-based text preprocessing
- TF-IDF Vectorization for feature extraction
- Modern Streamlit UI for ease of use

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Train the model and vectorizer:
   ```bash
   python train.py
   ```
2. Run the application:
   ```bash
   streamlit run app.py
   ```

## How it Works
The model is trained on the `spam_ham_dataset.csv`. It uses a **Logistic Regression** classifier combined with **TF-IDF Vectorization** to analyze text patterns common in spam emails.

## License
MIT License
