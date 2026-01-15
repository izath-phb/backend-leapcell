from dotenv import load_dotenv
load_dotenv()

import pymysql
pymysql.install_as_MySQLdb()

import os
import warnings

# ===============================
# SUPPRESS ALL WARNINGS
# ===============================
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore")

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    # init extensions
    db.init_app(app)
    jwt.init_app(app)

    # === IMPORT BLUEPRINT ===
    from routes.auth import auth
    from routes.body_detection import detection
    from routes.feedback import feedback
    from routes.chatbot import chatbot
    from routes.admin_dashboard import admin_dashboard
    from routes.lifestyle import lifestyle
    from routes.food_detection import food
    from routes.admin_users import admin_users
    from routes.admin_bmi import admin_bmi

    # === REGISTER BLUEPRINT ===
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(detection, url_prefix='/api/detection')
    app.register_blueprint(feedback, url_prefix='/api/feedback')
    app.register_blueprint(chatbot, url_prefix='/api/chatbot')
    app.register_blueprint(admin_dashboard, url_prefix='/api/admin/dashboard')
    app.register_blueprint(lifestyle, url_prefix='/api/lifestyle')
    app.register_blueprint(food, url_prefix='/api/food')
    app.register_blueprint(admin_users, url_prefix='/api/admin')
    app.register_blueprint(admin_bmi, url_prefix='/api/admin')

    # === CREATE TABLE (DEV ONLY) ===
    if os.getenv("FLASK_ENV") == "development":
        with app.app_context():
            db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
