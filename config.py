import os

class Config:
    SECRET_KEY = "smart-health-sense-secret"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://smarthea_izath:Izath.123@195.88.211.170/smarthea_smart_health_sense"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-smart-health-sense"
    UPLOAD_FOLDER = "static/uploads"

    # # Hugging Face Token
    # HF_TOKEN = os.getenv("HF_TOKEN")

    # # Repo ID (bukan API URL)
    # HF_FOOD_REPO = "izath/food_detection"
    # HF_BODY_REPO = "izath/body_detection"

    # HF Inference API (chatbot)
    HF_CHATBOT_API = "https://api-inference.huggingface.co/models/izath/chatbot"
