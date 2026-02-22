from app import base
from datetime import datetime
from flask_login import UserMixin

# 1. Tabela de Usuários
class userModel(base.Model, UserMixin):
    __tablename__ = 'users' # Nome explícito da tabela
    id = base.Column(base.Integer, primary_key=True)
    nome = base.Column(base.String, nullable=True)
    sobrenome = base.Column(base.String, nullable=True)
    email = base.Column(base.String, unique=True, nullable=True)
    senha = base.Column(base.String, nullable=True)
    telefone = base.Column(base.String, nullable=True)
    data = base.Column(base.DateTime, default=datetime.utcnow)
    balance = base.Column(base.Float, default=1000.0)  # Saldo inicial para novos usuários
    
    motor_id = base.Column(base.Integer, base.ForeignKey('motors.id'), default=0)
    
    # Relações usando os nomes das classes (Strings)
    investimentos = base.relationship('investmentModel', backref='investidor', lazy=True)
    depositos = base.relationship('depositModel', backref='cliente', lazy=True)
    saques = base.relationship('withdrawModel', backref='beneficiario', lazy=True)
    vendas = base.relationship('saleModel', backref='comprador', lazy=True)
    historico_motores = base.relationship('motorUpgradeModel', backref='investidor', lazy=True)
    pix = base.relationship('pixModel', backref='cliente', lazy=True)

# 2. Tabela de Configuração de Motores
class motorModel(base.Model):
    __tablename__ = 'motors'
    id = base.Column(base.Integer, primary_key=True)
    name = base.Column(base.String, nullable=False)
    upgrade_cost = base.Column(base.Float, nullable=False)
    usuarios = base.relationship('userModel', backref='motor_atual', lazy=True)

    # 8. Tabela de Log de Upgrades (Histórico de Evolução)
class motorUpgradeModel(base.Model):
    __tablename__ = 'motor_upgrades'
    id = base.Column(base.Integer, primary_key=True)
    user_id = base.Column(base.Integer, base.ForeignKey('users.id'), nullable=False)
    motor_id = base.Column(base.Integer, base.ForeignKey('motors.id'), nullable=False)
    valor_pago = base.Column(base.Float, nullable=False)
    data_upgrade = base.Column(base.DateTime, default=datetime.utcnow)
    motor = base.relationship('motorModel', backref='vendas_deste_nivel', lazy=True)
    # RELAÇÕES: Permite fazer upgrade.motor.name ou upgrade.investidor.nome
    # (O backref 'historico_motores' permite que o User aceda a esta tabela)

# 3. Tabela de Depósitos
class depositModel(base.Model):
    __tablename__ = 'deposits'
    id = base.Column(base.Integer, primary_key=True)
    user_id = base.Column(base.Integer, base.ForeignKey('users.id'), nullable=False)
    amount = base.Column(base.Float, nullable=False)
    proof_url = base.Column(base.String, nullable=True)
    status = base.Column(base.String, default='Pendente') 
    created_at = base.Column(base.DateTime, default=datetime.utcnow)

# 4. Tabela de Saques
class withdrawModel(base.Model):
    __tablename__ = 'withdraws'
    id = base.Column(base.Integer, primary_key=True)
    user_id = base.Column(base.Integer, base.ForeignKey('users.id'), nullable=True)
    amount = base.Column(base.Float, nullable=True)
    bank_details = base.Column(base.Text, nullable=True)
    status = base.Column(base.String, default='Pendente')
    created_at = base.Column(base.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.amount}'

# 5. Tabela de Investimentos
class investmentModel(base.Model):
    __tablename__ = 'investments'
    id = base.Column(base.Integer, primary_key=True)
    user_id = base.Column(base.Integer, base.ForeignKey('users.id'), nullable=False)
    amount = base.Column(base.Float, nullable=False)
    expected_return = base.Column(base.Float, nullable=False)
    start_date = base.Column(base.DateTime, default=datetime.utcnow)
    end_date = base.Column(base.DateTime, nullable=False)
    active = base.Column(base.Boolean, default=True)

# 6. Tabela do Marketplace
class productModel(base.Model):
    __tablename__ = 'products'
    id = base.Column(base.Integer, primary_key=True)
    name = base.Column(base.String, nullable=False)
    description = base.Column(base.Text, nullable=True)
    price = base.Column(base.Float, nullable=False)
    image_url = base.Column(base.String, nullable=True)
    stock = base.Column(base.Integer, default=0)
    
    historico_vendas = base.relationship('saleModel', backref='produto_detalhe', lazy=True)

# 7. Tabela de Vendas
class saleModel(base.Model):
    __tablename__ = 'sales'
    id = base.Column(base.Integer, primary_key=True)
    user_id = base.Column(base.Integer, base.ForeignKey('users.id'), nullable=False)
    product_id = base.Column(base.Integer, base.ForeignKey('products.id'), nullable=False)
    total_price = base.Column(base.Float, nullable=False)
    created_at = base.Column(base.DateTime, default=datetime.utcnow)

# Tabela Admin
class admiModel(base.Model, UserMixin):
    __tablename__ = 'admins'
    id = base.Column(base.Integer, primary_key=True)
    nome = base.Column(base.String, nullable=True)
    sobrenome = base.Column(base.String, nullable=True)
    email = base.Column(base.String, unique=True, nullable=True)
    senha = base.Column(base.String, nullable=True)
    telefone = base.Column(base.String, nullable=True)

# Tabela de Pix
class pixModel(base.Model):
    __tablename__ = 'pix'
    id = base.Column(base.Integer, primary_key=True)
    nome = base.Column(base.String, nullable=True)
    conta = base.Column(base.String, nullable=True)
    id_user = base.Column(base.Integer, base.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return f' {self.nome} - {self.conta}'