from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.body_detection import BodyDetection
from flask_cors import CORS
from sqlalchemy import text 

# === Blueprint ===
admin_bmi = Blueprint('admin_bmi', __name__)
CORS(admin_bmi, resources={r"/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

# === Helper untuk cek admin ===
def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'

# === Handle preflight OPTIONS ===
@admin_bmi.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

# === Route: BMI Terbaru ===
@admin_bmi.route('/bmi/latest', methods=['GET'])
@jwt_required()
def latest_bmi():
    try:
        admin_id = get_jwt_identity()
        if not is_admin(admin_id):
            return jsonify({"message": "Admin only"}), 403

        rows = db.session.execute(text("""
        SELECT user_id, email, bmi, category, created_at
        FROM view_latest_bmi
        ORDER BY created_at DESC
        """)).fetchall()

        bmi_list = []
        for row in rows:
            bmi_list.append({
                "user_id": row[0],
                "email": row[1],
                "bmi": row[2],
                "category": row[3],
                "created_at": row[4].isoformat() if row[4] else None
            })

        return jsonify(bmi_list), 200

    except Exception as e:
        print("Error latest_bmi:", e)
        import traceback; traceback.print_exc()
        return jsonify({"message": "Terjadi kesalahan server"}), 500

# === Route: Statistik BMI ===
@admin_bmi.route('/bmi/statistics', methods=['GET'])
@jwt_required()
def bmi_statistics():
    try:
        admin_id = get_jwt_identity()

        if not is_admin(admin_id):
            return jsonify({"message": "Admin only"}), 403

        result = db.session.execute("""
            SELECT category, total
            FROM view_bmi_statistics
        """).fetchall()

        stats_list = [dict(row._mapping) for row in result]

        return jsonify(stats_list), 200

    except Exception as e:
        print("Error bmi_statistics:", e)
        return jsonify({"message": "Terjadi kesalahan pada server"}), 500
