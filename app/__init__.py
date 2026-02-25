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
# Define o caminho absoluto para a pasta de imagens
# Isso aponta para app/static/data/img/
UPLOAD_FOLDER = os.path.join(aplication.root_path, 'static', 'data', 'img')

# Cria a pasta caso ela não exista (muito importante!)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

aplication.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        # Configuração do caminho absoluto para a pasta de uploads
        # Isso cria um caminho como: seu_projeto/static/uploads/post
        #UPLOAD_FOLDER = os.path.join(aplication.root_path, 'static', 'uploads', 'post')
        #aplication.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # Engenharia de Segurança: Garantir que a pasta exista ao iniciar o servidor
        #if not os.path.exists(aplication.config['UPLOAD_FOLDER']):
         #   os.makedirs(aplication.config['UPLOAD_FOLDER'])

base = SQLAlchemy(aplication)
mig = Migrate(aplication, base)
Login_manager = LoginManager(aplication)
Login_manager.login_view = 'home'
bcrypt = Bcrypt(aplication)

@Login_manager.user_loader
def load_user(id):
    return userModel.query.get(int(id))


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
