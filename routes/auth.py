from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.user import User
from models.jwt_blacklist import JWTBlacklist
from extensions import db
from datetime import timedelta
from firebase_admin import auth as firebase_auth
from models.user_body_metrics import UserBodyMetrics

auth = Blueprint('auth', __name__)

# ======================
# REGISTER
# ======================
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"message": "Name, email & password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409

    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role="user"  
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Register success",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201

# ======================
# LOGIN EMAIL
# ======================
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

# ======================
# LOGIN GOOGLE
# ======================
@auth.route('/google', methods=['POST'])
def google_login():
    token = request.json.get('id_token')

    if not token:
        return jsonify({"message": "Firebase ID token required"}), 400

    decoded = firebase_auth.verify_id_token(token)
    email = decoded.get('email')
    firebase_uid = decoded.get('uid')

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            name=email.split('@')[0],
            email=email,
            google_id=firebase_uid,
            role="user"
        )
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name, 
            "email": user.email,
            "role": user.role
        }
    }), 200

# ======================
# PROFILE
# ======================
@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    latest_bmi = UserBodyMetrics.query \
        .filter_by(user_id=user_id) \
        .order_by(UserBodyMetrics.created_at.desc()) \
        .first()

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "latest_bmi": {
            "bmi": latest_bmi.bmi if latest_bmi else None,
            "category": latest_bmi.bmi_category if latest_bmi else None,
            "height_cm": latest_bmi.height_cm if latest_bmi else None,
            "weight_kg": latest_bmi.weight_kg if latest_bmi else None,
            "age": latest_bmi.age if latest_bmi else None,
            "gender": latest_bmi.gender if latest_bmi else None,
            "created_at": latest_bmi.created_at if latest_bmi else None
        }
    }), 200

# ======================
# LOGOUT
# ======================
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    db.session.add(JWTBlacklist(jti=jti))
    db.session.commit()
    return jsonify({"message": "Logged out"}), 200
