from extensions import db
from datetime import datetime

class UserBodyMetrics(db.Model):
    __tablename__ = 'user_body_metrics'

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='gender_enum'), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)

    bmi = db.Column(db.Float, nullable=False)
    bmi_category = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ======================
    # RELATIONSHIP
    # ======================
    user = db.relationship(
        'User',
        backref=db.backref(
            'body_metrics',
            lazy=True,
            cascade='all, delete-orphan'
        )
    )

    # ======================
    # SERIALIZER
    # ======================
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "bmi": round(self.bmi, 2),
            "bmi_category": self.bmi_category,
            "created_at": self.created_at.isoformat()
        }
