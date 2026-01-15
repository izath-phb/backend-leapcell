import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from extensions import db
from models.body_detection import BodyDetection
from models.user_profile import UserProfile
# from cnn_model.predict import predict_body
from config import Config

detection = Blueprint('detection', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        return bmi, 'underweight'
    elif bmi < 25:
        return bmi, 'normal'
    elif bmi < 30:
        return bmi, 'overweight'
    else:
        return bmi, 'obese'


@detection.route('/upload', methods=['POST'])
@jwt_required()
def upload_body_image():
    user_id = int(get_jwt_identity())  

    if 'image' not in request.files:
        return jsonify({"message": "No image uploaded"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Invalid file type"}), 400

    filename = secure_filename(file.filename) # type: ignore
    upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    file.save(upload_path)

    # === Ambil profil user ===
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"message": "User profile not found"}), 404

    # === CNN BODY SHAPE ===
    cnn_category, confidence = predict_body(upload_path)

    # === BMI ILMIAH ===
    bmi_value, bmi_category = calculate_bmi(
        profile.weight_kg,
        profile.height_cm
    )

    detection_data = BodyDetection(
    user_id=user_id, # type: ignore
    image_path=upload_path, # type: ignore
    bmi=bmi_value, # type: ignore
    category=cnn_category, # type: ignore
    model_version='cnn-v1' # type: ignore
    )


    db.session.add(detection_data)
    db.session.commit()

    return jsonify({
        "message": "Body detection success",
        "cnn_prediction": cnn_category,
        "confidence": round(confidence * 100, 2),
        "bmi": bmi_value,
        "bmi_category": bmi_category
    }), 201
