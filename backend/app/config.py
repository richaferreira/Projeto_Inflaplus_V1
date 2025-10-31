
import os
from dotenv import load_dotenv
load_dotenv()

BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, '..', '..'))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'troque-por-um-valor-bem-aleatorio-e-seguro')
    WTF_CSRF_TIME_LIMIT = None

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(PROJECT_ROOT, 'infra_plus.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(FRONTEND_DIR, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif'}
