from app import aplication
from app.models import userModel,admiModel,motorModel, pixModel,depositModel
from app.forms import DepositForm, LoginAdminForm, LoginForm, UpdateUserForm, UpgradeMotorForm, UserForm,AdminForm,MotorForm, PixForm, SaqueForm
from flask import render_template,url_for, redirect, flash
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
    obj = obj = depositModel.query.filter_by(user_id=current_user.id, status='Pendente').first()
    return render_template('homeuser.html', obj=obj)


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


@aplication.route('/home/funcionamento/<int:id>', methods=['GET','POST'])
@login_required
def funcionamentoId(id):
    obj = motorModel.query.get_or_404(id)
    if current_user.balance < obj.upgrade_cost:
        flash('Saldo insuficiente para realizar o upgrade.', 'danger')
        form = UpgradeMotorForm()
        if form.validate_on_submit():
            return redirect(url_for('funcionamentoId', id=id))
        return render_template('motorUpgarde.html', form=form, obj=obj)
    return render_template('motorUpgarde.html', form = form, obj=obj)



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
    return render_template('admin.html')




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



@aplication.route('/deposito', methods=['GET', 'POST'])
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
    return render_template('deposito.html', obj=obj, form=form)




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
