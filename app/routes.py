import requests
from app import base
from datetime import datetime
from sqlalchemy import func

from app import aplication
from app.models import motorUpgradeModel, userModel,admiModel,motorModel, pixModel,depositModel, withdrawModel,userModel
from app.forms import DepositForm, LoginAdminForm, LoginForm, UpdateUserForm, UpgradeMotorForm, UserForm,AdminForm,MotorForm, PixForm, saqueForm
from flask import render_template, request,url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required



@aplication.route('/')
def homePage():
    return render_template('index.html')

@aplication.route('/sobre/')
def inforLogin():
    return render_template('info.html')

##############ROTAS DE USUÁRIO LOGADO HOME##############

@aplication.route('/home/')
@login_required
def home():
    obj = depositModel.query.filter_by(user_id=current_user.id, status='Pendente').first()
    upM = motorUpgradeModel.query.filter_by(user_id=current_user.id).order_by(motorUpgradeModel.data_upgrade.desc()).first()

    withdraw_sum = base.session.query(func.sum(withdrawModel.amount)).filter_by(
        user_id=current_user.id, status='Pendente'
    ).scalar() or 0
    withdrawC_sum = base.session.query(func.sum(withdrawModel.amount)).filter_by(
        user_id=current_user.id, status='Concluído'
    ).scalar() or 0
    withdraw = {'amount': withdraw_sum}
    withdrawC = {'amount': withdrawC_sum}
    if upM is None:
         data_motor = datetime.now().strftime("%Y-%m-%d")
         nome_motor = "Padrao"
         return render_template('homeuser.html', obj=obj, data_motor=data_motor, 
            nome_motor=nome_motor, withdraw=withdraw, withdrawC=withdrawC)
    else:
        return render_template('homeuser.html', obj=obj, upM=upM, 
            withdraw=withdraw, withdrawC=withdrawC)


@aplication.route('/home/clientes/')
@login_required
def cliente():
    return render_template('clientes.html')

@aplication.route('/home/info/')
@login_required
def infor():
    return render_template('informacao.html')

@aplication.route('/home/marketplace/')
@login_required
def marke():
    # Consumindo a API pública de produtos
    url_api = "https://fakestoreapi.com/products"
    
    try:
        response = requests.get(url_api, timeout=5)
        produtos = response.json() # Transforma a resposta em uma lista de dicionários
    except Exception as e:
        print(f"Erro ao conectar com a API: {e}")
        produtos = [] # Lista vazia para não quebrar a página caso a API caia

    return render_template('marketplace.html', produtos=produtos)


@aplication.route('/home/funcionamento/', methods=['POST', 'GET'])
@login_required
def funcionamento():
    obj = motorModel.query.all()
    return render_template('funcionamento.html', obj=obj)


@aplication.route('/home/funcionamento/<int:id>', methods=['GET', 'POST'])
@login_required
def funcionamentoId(id):
    obj = motorModel.query.get_or_404(id)
    form = UpgradeMotorForm()
    if form.validate_on_submit():
        if current_user.saldo_actual >= obj.upgrade_cost:
            try:
                debit = withdrawModel(
                    user_id=current_user.id, 
                    amount=obj.upgrade_cost,
                    status='Concluído')
                base.session.add(debit)
                current_user.motor_id = obj.id
                form.save(current_user.id, obj.id)  # Salva o upgrade no histórico
                base.session.commit()          
                flash(f'Upgrade do {obj.name} realizado com sucesso!', 'success')
                return redirect(url_for('funcionamentoId', id=id))

            except Exception as e:
                flash(f'Erro ao processar upgrade. Tente novamente. {e}', 'danger')
        else:
            flash('Saldo insuficiente para realizar o upgrade.', 'danger')
            return redirect(url_for('funcionamentoId', id=id))
    return render_template('motorUpgarde.html', form=form, obj=obj)





@aplication.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('home'))
    return render_template('login.html', form = form)


@aplication.route('/logout/', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homePage'))


##########ROTAS DE PERFIL E FORMULARIOS DE CADASTROS##############


@aplication.route('/register/', methods=['POST', 'GET'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('conta.html', form = form)

@aplication.route('/home/update/', methods=['POST', 'GET'])
@login_required
def updateuser():
    form = UpdateUserForm()
    if form.validate_on_submit():
        user = form.save(current_user)
        if user:
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('home'))
    return render_template('perfil.html', form = form)

@aplication.route('/motor/cadastrar/', methods=['POST', 'GET'])
def createmoor():
    form = MotorForm()
    if form.validate_on_submit():
        form.save()
    return render_template('motor.html', form = form)


@aplication.route('/home/configuracao/', methods=['POST', 'GET'])
@login_required
def confi_saq():
    form = PixForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('home'))
    return render_template('confi_saque.html', form =form)



@aplication.route('/home/extrato/')
@login_required
def extrato():
    # Procura todos os depósitos do utilizador atual, do mais novo para o mais velho
    historico = depositModel.query.filter_by(user_id=current_user.id).order_by(depositModel.created_at.desc()).all()
    
    return render_template('extrato.html', historico=historico)

#############################################################################
@aplication.route('/home/sacar/', methods=['GET', 'POST'])
@login_required
def sacar():

    form = saqueForm()
    if form.validate_on_submit():
        if form.amount.data > current_user.saldo_actual:
            flash("Erro: Saldo insuficiente para esta operação.", "danger")
        elif form.amount.data < 2000: # Exemplo de saque mínimo
            flash("Erro: O valor mínimo para saque é de 2000 Kz.", "warning")
        else:
            form.save(current_user.id)
            flash("Saque solicitado com sucesso! Aguarde a aprovação.", "success")      
    return render_template('sacar.html', form=form)


#################################################################







@aplication.route('/home/deposito/', methods=['GET', 'POST'])
@login_required
def deposito():
    form = DepositForm()
    if form.validate_on_submit():
        obj = depositModel.query.filter_by(user_id=current_user.id, status='Pendente').first()
        if obj:
            flash('Você já tem um depósito pendente!', 'warning')
        else:
            form.save(current_user.id)
            flash('Depósito enviado para análise!', 'success')
        return redirect(url_for('home'))
    return render_template('deposito.html', form=form)


@aplication.route('/admin/perfil/')
@login_required
def adminperfil():
    dp= depositModel.query.filter_by(status='Pendente').all()
    cp = sum(deposit.amount for deposit in depositModel.query.filter_by(status='Aprovado').all())

    sq = withdrawModel.query.filter_by(status='Pendente').all() 
    return render_template('admin.html', dp=dp, cp=cp, sq=sq)




@aplication.route('/admin/cadastrar/', methods=['POST', 'GET'])
def createadm():
    form = AdminForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('adminperfil'))
    return render_template('admiconta.html', form = form)


@aplication.route('/admin/', methods=['POST', 'GET'])
def loginadmin():
    form = LoginAdminForm()
    if form.validate_on_submit():
        adm = form.login()
        if adm:
            login_user(adm, remember=True)
            return redirect(url_for('adminperfil'))
    return render_template('loginAdmin.html', form = form)


##########################################################
#@aplication.route('/admin/users/', methods=['POST', 'GET'])
#@login_required
#def users():
#    obj = userModel.query.all()                               
#    return render_template('users.html', obj=obj)           #
#############################################################


from flask import render_template
from datetime import datetime, timedelta

@aplication.route('/admin/usuarios')
@login_required
def users():
    if not current_user.is_admin:
        return redirect(url_for('adminperfil'))
    page = request.args.get('page', 1, type=int)
    per_page = 10
    usuarios_paginados = userModel.query.paginate(page=page, per_page=per_page, error_out=False)
    lista_investidores = []
    for user in usuarios_paginados.items:
        motor = motorUpgradeModel.query.filter_by(user_id=user.id).order_by(motorUpgradeModel.data_upgrade.desc()).first()
        dias_passados = 0
        progresso_percent = 0
        nome_motor = motorModel.query.get(user.motor_id).name if user.motor_id else "Padrão"
        valor_investido = 0 # Você pode adaptar conforme sua lógica de preço de motor

        if motor:
            nome_motor = motor.motor.name
            delta = datetime.now() - motor.data_upgrade
            dias_passados = delta.days
            if dias_passados > 30: dias_passados = 30
            progresso_percent = (dias_passados / 31) * 100
            # Se tiver uma coluna de preço no seu modelo, use-a aqui:
            valor_investido = motor.motor.upgrade_cost # Exemplo, adapte conforme seu modelo 

        lista_investidores.append({
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'motor': nome_motor,
            'dias': dias_passados,
            'progresso': progresso_percent,
            'investimento': user.saldo_actual, # Usando a property que criamos antes
            'status': 'Ativo' if dias_passados < 31 else 'Concluído'
        })

    return render_template('users.html', investidores=lista_investidores, paginacao=usuarios_paginados)


@aplication.route('/admin/aprovar/')
@login_required
def aprovar():
    depositos = depositModel.query.all()
    dp= depositModel.query.filter_by(status='Pendente').all()
    if not current_user.is_admin:
        flash("Acesso negado ao núcleo do sistema.", "danger")
        return redirect(url_for('homePage'))
    return render_template('admin_panel.html', obj=userModel.query.all(), depositos=depositos, dp=dp)

@aplication.route('/admin/aprovar/<int:deposito_id>')
@login_required
def aprovar_deposito(deposito_id):

    if not current_user.is_admin: # Certifique-se de ter o campo 'is_admin' no modelo User
        flash("Acesso negado ao núcleo do sistema.", "danger")
        return redirect(url_for('homePage'))

    deposito = depositModel.query.get_or_404(deposito_id)
    
    if deposito.status == 'Pendente':
        # 1. Localizar o usuário dono do depósito
        usuario = userModel.query.get(deposito.user_id)
        
        # 2. Injeção de Capital (Atualização de Saldo)
        usuario.balance += deposito.amount
        
        # 3. Atualizar Status do Depósito
        deposito.status = 'Aprovado'
        
        base.session.commit()
        flash(f"Capital de {deposito.amount} Kz aprovado para {usuario.nome}!", "success")
    
    return redirect(url_for('aprovar'))

##########ROTAS DE PERFIL E FORMULARIOS DE CADASTROS##############











@aplication.route('/admin/saques')
@login_required
def admin_saques():
    if not current_user.is_admin:
        return redirect(url_for('adminperfil'))
    todos_saques = withdrawModel.query.order_by(withdrawModel.status.desc(), withdrawModel.created_at.desc()).all()
    return render_template('admin_saques.html', saques=todos_saques)

@aplication.route('/admin/pagar-saque/<int:saque_id>')
@login_required
def pagar_saque(saque_id):
    if not current_user.is_admin:
        return redirect(url_for('homePage'))

    saque = withdrawModel.query.get_or_404(saque_id)
    if saque.status == 'Pendente':
        saque.status = 'Concluído' # O saldo já foi abatido na @property do User
        base.session.commit()
        flash(f"Saque de {saque.amount} Kz marcado como Pago!", "success")
        
    return redirect(url_for('admin_saques'))
























@aplication.route('/meus-upgrades')
@login_required
def meus_upgrades():
    # Graças ao 'backref' que criamos (historico_motores), 
    # podemos aceder diretamente aos upgrades do utilizador
    lista_upgrades = current_user.historico_motores
    # Ou de forma explícita:
    # lista_upgrades = motorUpgradeModel.query.filter_by(user_id=current_user.id).order_by(motorUpgradeModel.data_upgrade.desc()).all()
    
    return render_template('upgrade.html', upgrades=lista_upgrades)
