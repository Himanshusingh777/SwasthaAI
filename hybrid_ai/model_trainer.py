import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'train_symptoms.csv')

def train_and_save():
    df = pd.read_csv(DATA_PATH)
    df['symptoms'] = df['symptoms'].astype(str)
    df['disease'] = df['disease'].astype(str)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), stop_words='english')),
        ('clf', MultinomialNB())
    ])
    pipeline.fit(df['symptoms'], df['disease'])
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_and_save()
