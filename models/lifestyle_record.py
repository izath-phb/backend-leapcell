from extensions import db
from datetime import datetime

class LifestyleRecord(db.Model):
    __tablename__ = 'lifestyle_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    water_intake_liter = db.Column(db.Float)
    drink_type = db.Column(db.String(50))
    sleep_hours = db.Column(db.Float)
    sleep_time = db.Column(db.Time)
    exercise_duration_min = db.Column(db.Integer)
    exercise_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
