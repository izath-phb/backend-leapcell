from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text
from extensions import db
from models.admin_log import AdminLog
from models.user import User
from models.user_profile import UserProfile

admin_dashboard = Blueprint('admin_dashboard', __name__)


def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'


@admin_dashboard.route('/summary', methods=['GET'])
@jwt_required()
def dashboard_summary():
    admin_id = get_jwt_identity()

    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    # ===============================
    # ADMIN INFO
    # ===============================
    admin = User.query.get(admin_id)
    profile = UserProfile.query.filter_by(user_id=admin.id).first()

    # ===============================
    # TOTAL USERS
    # ===============================
    total_users = db.session.execute(
        text("SELECT total_users FROM view_total_users")
    ).scalar()

    # ===============================
    # BMI STATISTICS
    # ===============================
    bmi_stats = db.session.execute(
        text("SELECT category, total FROM view_bmi_statistics")
    ).fetchall()

    # ===============================
    # FEEDBACK
    # ===============================
    avg_feedback = db.session.execute(
        text("SELECT feedback_type, avg_rating, total_feedback FROM view_avg_feedback")
    ).fetchall()

    # ===============================
    # CHATBOT ACTIVITY
    # ===============================
    chatbot_activity = db.session.execute(
        text("SELECT chat_date, total_chat FROM view_chatbot_activity")
    ).fetchall()

    # ===============================
    # LOG
    # ===============================
    db.session.add(AdminLog(
        admin_id=admin_id,
        action="View dashboard summary"
    ))
    db.session.commit()

    return jsonify({
        "admin": {
            "id": admin.id,
            "email": admin.email,
            "name": profile.name if profile else "Administrator"
        },

        "total_users": total_users,

        "bmi_statistics": [
            {"category": c, "total": t}
            for c, t in bmi_stats
        ],

        "avg_feedback": [
            {
                "type": f,
                "avg_rating": float(a),
                "total": t
            }
            for f, a, t in avg_feedback
        ],

        "chatbot_activity": [
            {
                "date": str(d),
                "total": t
            }
            for d, t in chatbot_activity
        ]
    }), 200
