import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "final_teen_mental_health_chatbot_dataset.csv")

df = pd.read_csv(data_path)

# Prepare data
user_inputs = df["user_input"].astype(str)
bot_responses = df["bot_response"].astype(str)

# Create TF-IDF model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(user_inputs)


def get_ml_response(user_message):
    user_vector = vectorizer.transform([user_message])
    similarities = cosine_similarity(user_vector, X)
    best_match_index = similarities.argmax()
    confidence = similarities[0][best_match_index]

    return {
        "response": bot_responses.iloc[best_match_index],
        "confidence_score": round(float(confidence), 3)
    }
