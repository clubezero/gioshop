import os
from app import base, bcrypt
from app.models import motorUpgradeModel, pixModel, userModel, admiModel, motorModel,withdrawModel
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

    def save(self, id):
        motor = motorModel(
            name = self.nome.data,
            upgrade_cost = self.upgrade_cost.data,
            id_user = id
        )

        base.session.add(motor)
        base.session.commit()

class PixForm(FlaskForm):
    nome = StringField('Nome do banco', validators=[data_required()])
    conta = StringField('IBAN', validators=[data_required()])
    btn = SubmitField('Salvar')

    def save(self, id_user):
        pix = pixModel(
            nome = self.nome.data,
            conta = self.conta.data,
            id_user = id_user
        )

        base.session.add(pix)
        base.session.commit()


class SaqueForm(FlaskForm):
    montante = StringField('Valor do Saque', validators=[data_required()])
    detalhes = StringField('Detalhes do Banco', validators=[data_required()])
    btn = SubmitField('Solicitar Saque')

    def save(self, id_user):
        saque = withdrawModel(
            user_id = id_user,
            amount = self.montante.data,
            bank_details = self.detalhes.data
        )

        base.session.add(saque)
        base.session.commit()


class UpgradeMotorForm(FlaskForm):
    valor_pago = IntegerField('Valor Pago', validators=[data_required()])
    def save(self, id_user, motor_id):
        upgrade = motorUpgradeModel(
            user_id = id_user,
            motor_id = motor_id,
            valor_pago = self.valor_pago.data
        )
        base.session.add(upgrade)
        base.session.commit()


