from extensions import db
from datetime import datetime

class BodyDetection(db.Model):
    __tablename__ = 'body_detections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_path = db.Column(db.String(255))
    bmi = db.Column(db.Float)
    category = db.Column(db.Enum('underweight','normal','overweight','obese'))
    model_version = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
