from extensions import db
from datetime import datetime

class ChatbotMessage(db.Model):
    __tablename__ = 'chatbot_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False) 
    user_message = db.Column(db.Text)
    bot_reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
