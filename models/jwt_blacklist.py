from extensions import db

class JWTBlacklist(db.Model):
    __tablename__ = 'jwt_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), unique=True)
