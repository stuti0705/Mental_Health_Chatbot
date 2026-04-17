import os
import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "train.csv")
MODEL_DIR = os.path.join(BASE_DIR, "ml")

# Load dataset
df = pd.read_csv(DATA_PATH)

# Extract HUMAN and ASSISTANT parts
questions = []
answers = []

for row in df["text"]:
    if "<HUMAN>:" in row and "<ASSISTANT>:" in row:
        parts = row.split("<ASSISTANT>:")
        question = parts[0].replace("<HUMAN>:", "").strip()
        answer = parts[1].strip()

        questions.append(question)
        answers.append(answer)

print(f"Loaded {len(questions)} question-answer pairs.")

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(questions)

# Save model
with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

with open(os.path.join(MODEL_DIR, "questions.pkl"), "wb") as f:
    pickle.dump(questions, f)

with open(os.path.join(MODEL_DIR, "answers.pkl"), "wb") as f:
    pickle.dump(answers, f)

print("Model training complete and saved.")
