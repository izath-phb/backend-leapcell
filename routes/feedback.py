from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.feedback import Feedback
from models.user import User

feedback = Blueprint('feedback', __name__)

# =========================
# SUBMIT FEEDBACK (USER)
# =========================
@feedback.route('', methods=['POST', 'OPTIONS'])
@jwt_required()
def submit_feedback():
    if request.method == 'OPTIONS':
        return '', 200

    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    rating = data.get('rating')
    feedback_type = data.get('feedback_type')
    comment = data.get('comment', '')

    if not rating or not feedback_type:
        return jsonify({"message": "Rating and feedback type are required"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    fb = Feedback(
        user_id=user_id,
        rating=rating,
        feedback_type=feedback_type,
        comment=comment
    )

    db.session.add(fb)
    db.session.commit()

    return jsonify({"message": "Feedback submitted successfully"}), 201


# =========================
# ADMIN CHECK
# =========================
def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'


# =========================
# LIST FEEDBACK (ADMIN)
# =========================
@feedback.route('/list', methods=['GET', 'OPTIONS'])
@jwt_required()
def list_feedback():
    if request.method == 'OPTIONS':
        return '', 200

    admin_id = int(get_jwt_identity())

    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()

    return jsonify([
        {
            "id": f.id,
            "user_id": f.user_id,
            "rating": f.rating,
            "type": f.feedback_type,
            "comment": f.comment,
            "date": f.created_at.strftime("%Y-%m-%d %H:%M")
        } for f in feedbacks
    ]), 200


# =========================
# UPDATE FEEDBACK (ADMIN)
# =========================
@feedback.route('/<int:id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_feedback(id):
    if request.method == 'OPTIONS':
        return '', 200

    admin_id = int(get_jwt_identity())

    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    fb = Feedback.query.get_or_404(id)
    data = request.get_json() or {}

    fb.rating = data.get('rating', fb.rating)
    fb.feedback_type = data.get('feedback_type', fb.feedback_type)
    fb.comment = data.get('comment', fb.comment)

    db.session.commit()

    return jsonify({"message": "Feedback updated"}), 200


# =========================
# DELETE FEEDBACK (ADMIN)
# =========================
@feedback.route('/<int:id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_feedback(id):
    if request.method == 'OPTIONS':
        return '', 200

    admin_id = int(get_jwt_identity())

    if not is_admin(admin_id):
        return jsonify({"message": "Admin only"}), 403

    fb = Feedback.query.get_or_404(id)
    db.session.delete(fb)
    db.session.commit()

    return jsonify({"message": "Feedback deleted"}), 200
