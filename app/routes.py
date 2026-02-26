from app import base

from app import aplication
from app.models import motorUpgradeModel, userModel,admiModel,motorModel, pixModel,depositModel, withdrawModel
from app.forms import DepositForm, LoginAdminForm, LoginForm, UpdateUserForm, UpgradeMotorForm, UserForm,AdminForm,MotorForm, PixForm, SaqueForm
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
    upM = motorUpgradeModel.query.filter_by(user_id=current_user.id).order_by(motorUpgradeModel.data_upgrade.desc()).first()
    obj = obj = depositModel.query.filter_by(user_id=current_user.id, status='Pendente').first()
    return render_template('homeuser.html', obj=obj, upM=upM)


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
    return render_template('marketplace.html')


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
        if current_user.balance >= obj.upgrade_cost:
            try:
                current_user.balance -= obj.upgrade_cost
                form.save(current_user.id, obj.id)  # Salva o upgrade no histórico           
                flash(f'Upgrade do {obj.nome} realizado com sucesso!', 'success')
                return redirect(url_for('funcionamentoId', id=id))
            
            except Exception as e:
                flash('Erro ao processar upgrade. Tente novamente.', 'danger')
        else:
            flash('Saldo insuficiente para realizar o upgrade.', 'danger')
            return redirect(url_for('funcionamentoId', id=id))

    return render_template('motorUpgarde.html', form=form, obj=obj)






#@aplication.route('/home/funcionamento/<int:id>', methods=['GET','POST'])
#@login_required
#def funcionamentoId(id):
#    obj = motorModel.query.get_or_404(id)
#    if current_user.balance < obj.upgrade_cost:
#        flash('Saldo insuficiente para realizar o upgrade.', 'danger')
#        form = UpgradeMotorForm()
#        if form.validate_on_submit():
#            return redirect(url_for('funcionamentoId', id=id))
#        return render_template('motorUpgarde.html', form=form, obj=obj)
#    return render_template('motorUpgarde.html', obj=obj)



############ROTAS DE LOGIN, LOGOUT##############

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


@aplication.route('/home/saque/', methods=['POST', 'GET'])
@login_required
def confi_saq():
    form = PixForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('home'))
    return render_template('confi_saque.html', form =form)

@aplication.route('/home/saque/', methods=['POST', 'GET'])
@login_required
def solicitar_saque():
    form = SaqueForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('home'))
    return render_template('solicitar_saque.html', form = form)



@aplication.route('/admin/perfil/')
@login_required
def adminperfil():
    dp= depositModel.query.filter_by(status='Pendente').all()
    cp = sum(deposit.amount for deposit in depositModel.query.filter_by(status='Aprovado').all())
    return render_template('admin.html', dp=dp, cp=cp)




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



@aplication.route('/admin/users/', methods=['POST', 'GET'])
@login_required
def users():
    obj = userModel.query.all()
    return render_template('users.html', obj=obj)



@aplication.route('/deposito/', methods=['GET', 'POST'])
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

@aplication.route('/home/extrato/')
@login_required
def extrato():
    # Procura todos os depósitos do utilizador atual, do mais novo para o mais velho
    historico = depositModel.query.filter_by(user_id=current_user.id).order_by(depositModel.created_at.desc()).all()
    
    return render_template('extrato.html', historico=historico)


@aplication.route('/home/sacar/', methods=['GET', 'POST'])
@login_required
def sacar():
    if request.method == 'POST':
        valor = float(request.form.get('amount'))
        iban = request.form.get('iban')
        
        # Validação Quântica de Saldo
        if valor > current_user.saldo_actual:
            flash("Erro: Saldo insuficiente para esta operação.", "danger")
        elif valor < 500: # Exemplo de saque mínimo
            flash("Erro: O valor mínimo para saque é de 500 Kz.", "warning")
        else:
            novo_saque = withdrawModel(
                user_id=current_user.id,
                amount=valor,
                iban=iban,
                status='Pendente'
            )
            base.session.add(novo_saque)
            base.session.commit()
            flash("Pedido de saque enviado com sucesso!", "success")
            return redirect(url_for('extrato'))
            
    return render_template('sacar.html')


@aplication.route('/admin/aprovar/')
@login_required
def aprovar():
    depositos = depositModel.query.all()
    dp= depositModel.query.filter_by(status='Pendente').all()
    if not current_user.is_admin:
        flash("Acesso negado ao núcleo do sistema.", "danger")
        return redirect(url_for('adminperfil'))
    return render_template('admin_panel.html', obj=userModel.query.all(), depositos=depositos, dp=dp)

@aplication.route('/admin/aprovar/<int:deposito_id>')
@login_required
def aprovar_deposito(deposito_id):

    if not current_user.is_admin: # Certifique-se de ter o campo 'is_admin' no modelo User
        flash("Acesso negado ao núcleo do sistema.", "danger")
        return redirect(url_for('home'))

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




































@aplication.route('/meus-upgrades')
@login_required
def meus_upgrades():
    # Graças ao 'backref' que criamos (historico_motores), 
    # podemos aceder diretamente aos upgrades do utilizador
    lista_upgrades = current_user.historico_motores
    # Ou de forma explícita:
    # lista_upgrades = motorUpgradeModel.query.filter_by(user_id=current_user.id).order_by(motorUpgradeModel.data_upgrade.desc()).all()
    
    return render_template('upgrade.html', upgrades=lista_upgrades)
