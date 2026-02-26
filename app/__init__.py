from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv('.env')
aplication = Flask(__name__)
aplication.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
aplication.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
aplication.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
UPLOAD_FOLDER = os.path.join(aplication.root_path, 'static', 'data', 'img')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
aplication.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


base = SQLAlchemy(aplication)
mig = Migrate(aplication, base)
Login_manager = LoginManager(aplication)
Login_manager.login_view = 'home'
bcrypt = Bcrypt(aplication)

@Login_manager.user_loader
def load_user(session_id):
    if not session_id:
        return None

    try:
        # O session_id virá como "user_1" ou "admin_1"
        # O .split("_", 1) divide a string no primeiro "_"
        prefix, user_id = session_id.split("_", 1)
        user_id = int(user_id) # Converte a parte do número para inteiro

        if prefix == "user":
            return userModel.query.get(user_id)
        elif prefix == "admin":
            return admiModel.query.get(user_id)
            
    except (ValueError, AttributeError):
        return None

    return None


def format_currency(value):
    if value is None:
        return "0,00"

    formatted = "{:,.2f}".format(float(value))
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
aplication.jinja_env.filters['format_currency'] = format_currency

from app.routes import homePage
from app.models import userModel
from app.models import motorModel
from app.models import motorUpgradeModel
from app.models import depositModel
from app.models import withdrawModel
from app.models import investmentModel
from app.models import productModel
from app.models import saleModel
from app.models import admiModel
from app.models import pixModel
