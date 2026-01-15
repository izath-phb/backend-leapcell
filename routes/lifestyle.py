from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.lifestyle_record import LifestyleRecord
from models.user_profile import UserProfile
from models.body_detection import BodyDetection
from models.health_recommendation import HealthRecommendation

lifestyle = Blueprint('lifestyle', __name__)


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = 'underweight'
    elif bmi < 25:
        category = 'normal'
    elif bmi < 30:
        category = 'overweight'
    else:
        category = 'obese'

    return bmi, category


@lifestyle.route('/record', methods=['POST'])
@jwt_required()
def create_lifestyle():
    user_id = get_jwt_identity()['id']
    data = request.json

    lifestyle = LifestyleRecord(
        user_id=user_id,
        water_intake_liter=data.get('water_intake_liter'),
        drink_type=data.get('drink_type'),
        sleep_hours=data.get('sleep_hours'),
        sleep_time=data.get('sleep_time'),
        exercise_duration_min=data.get('exercise_duration_min'),
        exercise_type=data.get('exercise_type')
    )

    db.session.add(lifestyle)

    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "User profile not found"}), 404

    bmi_value, category = calculate_bmi(profile.weight_kg, profile.height_cm)

    bmi_result = BodyDetection(
        user_id=user_id,
        bmi=bmi_value,
        category=category,
        model_version='manual-input'
    )

    db.session.add(bmi_result)

    recommendation_text = {
        'underweight': 'Increase calorie intake with healthy food.',
        'normal': 'Maintain your healthy lifestyle.',
        'overweight': 'Reduce sugar and increase physical activity.',
        'obese': 'Consult nutritionist and increase daily activity.'
    }

    recommendation = HealthRecommendation(
        user_id=user_id,
        bmi_category=category,
        recommendation=recommendation_text[category]
    )

    db.session.add(recommendation)
    db.session.commit()

    return jsonify({
        "message": "Lifestyle data saved",
        "bmi": bmi_value,
        "category": category,
        "recommendation": recommendation_text[category]
    }), 201
