import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY='846543d72e51fec5690c7fd527a4ec796d878d616c9dc3b3'
    SQLALCHEMY_DATABASE_URI='postgresql://flask_user:12345@localhost/bookdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}