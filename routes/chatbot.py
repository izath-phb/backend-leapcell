from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.chatbot_knowledge import ChatbotKnowledge
from models.chatbot_message import ChatbotMessage
from services.chatbot_llm import ask_llm

chatbot = Blueprint('chatbot', __name__)


def find_answer(user_question):
    result = ChatbotKnowledge.query.filter(
        ChatbotKnowledge.question.ilike(f"%{user_question}%")
    ).first()

    if result:
        return result.answer, result.category
    else:
        return "Maaf, saya belum memiliki jawaban untuk pertanyaan tersebut.", "unknown"


@chatbot.route('/ask', methods=['POST'])
@jwt_required()
def ask_chatbot():
    user_id = get_jwt_identity()
    data = request.json

    user_message = data.get('message')
    if not user_message:
        return jsonify({"message": "Message is required"}), 400

    # 1️⃣ Cari di knowledge base
    bot_reply, category = find_answer(user_message)

    # 2️⃣ Kalau tidak ketemu → pakai LLM
    if category == "unknown":
        try:
            bot_reply = ask_llm(user_message)
            category = "llm"

            new_knowledge = ChatbotKnowledge(
                question=user_message,
                answer=bot_reply,
                category="generated"
            )
            db.session.add(new_knowledge)

        except Exception as e:
            bot_reply = "Maaf, layanan AI sedang bermasalah."
            category = "error"

    # 3️⃣ Simpan chat history
    chat = ChatbotMessage(
        user_id=user_id,
        user_message=user_message,
        bot_reply=bot_reply
    )

    db.session.add(chat)
    db.session.commit()

    return jsonify({
        # "user_message": user_message,
        "bot_reply": bot_reply,
        "category": category
    }), 200
