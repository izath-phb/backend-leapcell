from extensions import db
from datetime import datetime

class HealthRecommendation(db.Model):
    __tablename__ = 'health_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bmi_category = db.Column(db.Enum('underweight','normal','overweight','obese'))
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
