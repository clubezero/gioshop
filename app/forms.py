import os
from app import base, bcrypt,aplication
from app.models import depositModel, motorUpgradeModel, pixModel, userModel, admiModel, motorModel,withdrawModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, FloatField
from wtforms.validators import DataRequired, data_required,Email,ValidationError, NumberRange
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed


class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[data_required()])
    sobrenome = StringField('Sobrenome', validators=[data_required()])
    email = StringField('E-Mail', validators=[data_required(), Email()])
    senha = PasswordField('Palavra-Passe', validators=[data_required()])
    telefone = StringField('Número de telefone', validators=[data_required()])
    btn = SubmitField('Criar conta')

    # Este método é chamado automaticamente pelo Flask-WTF durante form.validate_on_submit()
    def validate_email(self, email):
        user = userModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este e-mail já está em uso. Por favor, escolha outro.')

    def save(self):
        # A lógica de hash e commit permanece aqui, 
        # mas agora só será executada se validate_email passar.
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = userModel(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha_hash,
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
            
class LoginAdminForm(FlaskForm):
    email = StringField('E-Mail', validators=[data_required(), Email()])
    senha = PasswordField('Palavra-Passe', validators=[data_required()])
    btn = SubmitField('Entrar como Admin')

    def login(self):
        admin = admiModel.query.filter_by(email = self.email.data).first()
        if admin:
            if bcrypt.check_password_hash(admin.senha, self.senha.data.encode('utf-8')):
                return admin

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
    btn = SubmitField('Realizar Upgrade')

    def save(self, id_user, motor_id):
        upgrade = motorUpgradeModel(
            user_id = id_user,
            motor_id = motor_id,
        )
        try:
            base.session.add(upgrade)
            base.session.commit()
        except Exception as e:
            base.session.rollback()
            raise e




class UpdateUserForm(FlaskForm):
    nome = StringField('Nome', validators=[data_required()])
    sobrenome = StringField('Sobrenome', validators=[data_required()])
    email = StringField('E-Mail', validators=[data_required(), Email()])
    telefone = StringField('Número de telefone', validators=[data_required()])
    # Adicionamos filtro para aceitar apenas imagens
    imagem = FileField('Imagem de Perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens (jpg, png) são permitidas!')
    ])
    btn = SubmitField('Atualizar Perfil')

    # Validador para não permitir e-mail duplicado de outros usuários
    def validate_email(self, email):
        # Importante: só gera erro se o e-mail for de OUTRO usuário
        from flask_login import current_user
        user = userModel.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('Este e-mail já está sendo usado por outra conta.')

    def save(self, user):
        """
        Atualiza os dados do usuário e gerencia o ciclo de vida do arquivo de imagem.
        """
        # 1. Processamento da Nova Imagem (Se enviada)
        if self.imagem.data:
            arquivo = self.imagem.data
            nome_original = secure_filename(arquivo.filename)
            
            # Criamos um nome único para evitar conflito de cache no navegador
            # Ex: 1_perfil.jpg
            nome_final = f"{user.id}_{nome_original}"
            
            # Caminho absoluto usando o root_path para evitar erros de "Not Found"
            diretorio = os.path.join(aplication.root_path, 'static', 'data', 'img', 'post')
            os.makedirs(diretorio, exist_ok=True)

            # --- LÓGICA DE LIMPEZA (Manutenção de Entropia do Disco) ---
            # Removemos a imagem antiga para não acumular lixo no servidor
            if user.avatar and user.avatar != 'default.png':
                caminho_antigo = os.path.join(diretorio, user.avatar)
                if os.path.exists(caminho_antigo):
                    try:
                        os.remove(caminho_antigo)
                    except Exception as e:
                        print(f"Erro ao deletar: {e}")

            # Salvar o novo arquivo
            caminho_completo = os.path.join(diretorio, nome_final)
            arquivo.save(caminho_completo)
            
            # Atualiza o atributo no banco
            user.avatar = nome_final

        # 2. Atualizar demais campos (Mapeamento de Estado)
        user.nome = self.nome.data
        user.sobrenome = self.sobrenome.data
        user.email = self.email.data
        user.telefone = self.telefone.data

        # 3. Persistência de Dados
        try:
            base.session.commit()
            return True
        except Exception as e:
            base.session.rollback()
            print(f"Erro no commit: {e}")
            return False
        

class DepositForm(FlaskForm):
    amount = FloatField('Valor do Depósito (Kz)', validators=[
        DataRequired(message="Informe o valor"),
        NumberRange(min=2000, message="O depósito mínimo é de 2000 Kz")
    ])
    proof = FileField('Comprovante de Transferência', validators=[DataRequired(message="O comprovante é obrigatório")])
    btn = SubmitField('ENVIAR PARA ANÁLISE')

    def save(self, id_user):
        # Processamento do arquivo de comprovante
        arquivo = self.proof.data
        nome_original = secure_filename(arquivo.filename)
        nome_final = f"{id_user}_{nome_original}"
        
        diretorio = os.path.join(aplication.root_path, 'static', 'data', 'img', 'comprovantes')
        os.makedirs(diretorio, exist_ok=True)

        caminho_completo = os.path.join(diretorio, nome_final)
        arquivo.save(caminho_completo)

        # Criar registro de depósito
        deposito = depositModel(
            user_id = id_user,
            amount = self.amount.data,
            proof_url = f"data/img/comprovantes/{nome_final}"
        )

        base.session.add(deposito)
        base.session.commit()