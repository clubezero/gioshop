import os
from app import base, bcrypt
from app.models import userModel, admiModel, motorModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField,IntegerField
from wtforms.validators import data_required,Email
from werkzeug.utils import secure_filename


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[data_required()])
    sobrenome = StringField('Sobrenome', validators=[data_required()])
    email = StringField('E-Mail', validators=[data_required(), Email()])
    senha = PasswordField('Palavra-Passe', validators=[data_required()])
    telefone = StringField('Número de telefone', validators=[data_required()])
    btn = SubmitField('Criar conta')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = userModel(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha,
            telefone = self.telefone.data
        )

        base.session.add(user)
        base.session.commit()
        return user
        
class AdminForm(FlaskForm):
    nome = StringField('Nome', validators=[data_required()])
    sobrenome = StringField('Sobrenome', validators=[data_required()])
    email = StringField('E-Mail', validators=[data_required(), Email()])
    senha = PasswordField('Palavra-Passe', validators=[data_required()])
    telefone = StringField('Número de telefone', validators=[data_required()])
    btn = SubmitField('Criar conta')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        admi = admiModel(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha,
            telefone = self.telefone.data
        )

        base.session.add(admi)
        base.session.commit()
        return admi


class LoginForm(FlaskForm):
    telefone = StringField('Número de telefone', validators=[data_required()])
    senha = PasswordField('Palavra-Passe', validators=[data_required()])
    btn = SubmitField('Acessar o meu negocio')

    def login(self):
        user = userModel.query.filter_by(telefone = self.telefone.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user

class MotorForm(FlaskForm):
    nome = StringField('Nome do Motor', validators=[data_required()])
    upgrade_cost = IntegerField('Custo de Upgrade', validators=[data_required()])
    btn = SubmitField('Adicionar Motor')

    def save(self):
        motor = motorModel(
            name = self.nome.data,
            upgrade_cost = self.upgrade_cost.data,
        )

        base.session.add(motor)
        base.session.commit()
