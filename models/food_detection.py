from extensions import db
from datetime import datetime

class FoodDetection(db.Model):
    __tablename__ = 'food_detections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    food_name = db.Column(db.String(100))
    calories = db.Column(db.Float)
    portion_size = db.Column(db.String(50))
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
