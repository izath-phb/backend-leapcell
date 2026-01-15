from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from extensions import db
from models.user import User
from models.admin_log import AdminLog

admin_users = Blueprint('admin_users', __name__)


def is_admin(user_id):
    user = User.query.get(int(user_id))
    return user and user.role == 'admin'


# ================================
# GET ALL USERS
# ================================
@admin_users.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "id": u.id,
            "name": u.name, 
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "login_type": "google" if u.google_id else "email"
        }
        for u in users
    ]), 200

# ================================
# CREATE USER (ADMIN)
# ================================
@admin_users.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    admin_id = get_jwt_identity()
    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    data = request.get_json(force=True)

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        return jsonify({"message": "Email & password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    new_user = User(
        name=name,  
        email=email,
        password=generate_password_hash(password),
        role=role,
        is_active=True
    )

    db.session.add(new_user)
    db.session.commit()

    db.session.add(AdminLog(
        admin_id=int(admin_id),
        action=f"Create user {email}"
    ))
    db.session.commit()

    return jsonify({"message": "User created"}), 201

# ================================
# UPDATE USER (FULL EDIT)
# ================================
@admin_users.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    admin_id = get_jwt_identity()
    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json(force=True)

    # === UPDATE FIELD YANG DIKIRIM ===
    if "name" in data:
        user.name = data["name"]
        
    if "email" in data:
        user.email = data["email"]

    if "role" in data:
        user.role = data["role"]

    if "password" in data and data["password"]:
        user.password = generate_password_hash(data["password"])

    if "is_active" in data:
        user.is_active = data["is_active"]

    db.session.commit()

    db.session.add(AdminLog(
        admin_id=int(admin_id),
        action=f"Edit user ID {user_id}"
    ))
    db.session.commit()

    return jsonify({"message": "User updated"}), 200


# ================================
# DELETE USER
# ================================
@admin_users.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    admin_id = get_jwt_identity()
    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    db.session.add(AdminLog(
        admin_id=int(admin_id),
        action=f"Delete user ID {user_id}"
    ))
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200
