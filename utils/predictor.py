import os
import joblib

# ---------------------------
# Load Mental Health Classifier
# ---------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "ml", "mental_health_classifier.pkl")

classifier = joblib.load(model_path)


# ---------------------------
# Prediction Function
# ---------------------------

def predict_symptoms(user_message):

    predicted_class = classifier.predict([user_message])[0]
    probabilities = classifier.predict_proba([user_message])[0]
    class_labels = classifier.classes_

    prob_dict = {
        class_labels[i]: round(float(probabilities[i]), 3)
        for i in range(len(class_labels))
    }

    confidence_score = max(probabilities)
    suicidal_score = prob_dict.get("Suicidal", 0)

    # ---------------------------
    # Crisis Detection Logic
    # ---------------------------

    crisis_alert = False
    risk_level = "LOW"
    emergency_message = None

    if suicidal_score >= 0.30:
        crisis_alert = True
        risk_level = "HIGH"
        emergency_message = (
            "If you are feeling unsafe or thinking about harming yourself, "
            "please contact a suicide helpline immediately. "
            "In India: Call 9152987821 (Kiran Mental Health Helpline). "
            "If in immediate danger, call emergency services."
        )

    elif suicidal_score >= 0.15:
        risk_level = "MODERATE"

    # ---------------------------
    # Final Response
    # ---------------------------

    response_message = (
        f"Based on your message, you may be experiencing signs of {predicted_class}."
    )

    return {
        "response": response_message,
        "symptoms_detected": {
            "predicted_condition": predicted_class,
            "confidence_score": round(float(confidence_score), 3),
            "all_probabilities": prob_dict
        },
        "risk_level": risk_level,
        "crisis_alert": crisis_alert,
        "emergency_message": emergency_message
    }
