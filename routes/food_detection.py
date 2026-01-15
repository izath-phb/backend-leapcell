import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from extensions import db
from models.food_detection import FoodDetection
from models.body_detection import BodyDetection
# from cnn_model.food_predict import predict_food
from utils.food_calories import FOOD_CALORIES
from config import Config

food = Blueprint('food', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@food.route('/detect-cnn', methods=['POST'])
@jwt_required()
def detect_food_cnn():
    user_id = get_jwt_identity()['id']

    if 'image' not in request.files:
        return jsonify({"message": "No image uploaded"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"message": "No selected image"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Invalid image type"}), 400

    filename = secure_filename(file.filename)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(image_path)

    # === CNN Prediction ===
    # food_name, confidence = predict_food(image_path)

    # calories = FOOD_CALORIES.get(food_name, 0)

    # === Ambil BMI Terakhir ===
    bmi_data = BodyDetection.query.filter_by(user_id=user_id)\
        .order_by(BodyDetection.created_at.desc()).first()

    if bmi_data and bmi_data.category in ['overweight', 'obese']:
        recommendation = "Reduce portion and avoid fried food"
    else:
        recommendation = "Safe to consume in moderation"

    record = FoodDetection(
        user_id=user_id,
        # food_name=food_name,
        # calories=calories,
        portion_size="1 serving",
        recommendation=recommendation
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        # "food": food_name,
        # "confidence": confidence,
        # "calories": calories,
        "recommendation": recommendation
    }), 201
