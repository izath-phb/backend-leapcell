from extensions import db

class ChatbotKnowledge(db.Model):
    __tablename__ = 'chatbot_knowledge'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    category = db.Column(db.String(50))
