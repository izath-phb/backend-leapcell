from extensions import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female'))
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
