from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.predictor import predict_symptoms
from database.models import ChatHistory
from extensions import db

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()

    data = request.get_json()
    user_message = data.get("message", "")

    result = predict_symptoms(user_message)

    # Save to database
    new_chat = ChatHistory(
        user_id=user_id,
        user_message=user_message,
        bot_response=result["response"],
        confidence_score=result["symptoms_detected"].get("confidence_score")
    )

    db.session.add(new_chat)
    db.session.commit()

    return jsonify({
    "user_id": user_id,
    "response": result["response"],
    "symptoms_detected": result["symptoms_detected"],
    "risk_level": result.get("risk_level"),
    "crisis_alert": result.get("crisis_alert"),
    "emergency_message": result.get("emergency_message")
})

