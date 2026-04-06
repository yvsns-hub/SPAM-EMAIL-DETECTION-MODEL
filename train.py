import pandas as pd
import numpy as np
import string
import pickle
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Download NLTK data
nltk.download('stopwords')

def remove_stopwords(text, stop_words):
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)

def train_model():
    # Load dataset
    df = pd.read_csv('spam_ham_dataset.csv')
    
    # Preprocessing
    df['text'] = df['text'].str.lower()
    df['text'] = df['text'].str.translate(str.maketrans('', '', string.punctuation))
    
    stop_words = set(stopwords.words('english'))
    df['text'] = df['text'].apply(lambda x: remove_stopwords(x, stop_words))
    
    # Label encoding: spam -> 0, ham -> 1 (as per original notebook)
    df['label_num'] = df['label'].map({'spam': 0, 'ham': 1})
    
    X = df['text']
    Y = df['label_num']
    
    # Train-Test Split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)
    
    # Feature Extraction
    tfidf = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)
    X_train_features = tfidf.fit_transform(X_train)
    X_test_features = tfidf.transform(X_test)
    
    # Model Training
    model = LogisticRegression()
    model.fit(X_train_features, Y_train)
    
    # Evaluate
    train_acc = accuracy_score(Y_train, model.predict(X_train_features))
    test_acc = accuracy_score(Y_test, model.predict(X_test_features))
    
    print(f'Training Accuracy: {train_acc:.4f}')
    print(f'Testing Accuracy: {test_acc:.4f}')
    
    # Save model and vectorizer
    with open('spam_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    
    print("Model and Vectorizer saved successfully.")

if __name__ == "__main__":
    train_model()
