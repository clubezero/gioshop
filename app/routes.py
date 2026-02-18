from app import aplication
from app.models import userModel,admiModel,motorModel
from app.forms import LoginForm, UserForm,AdminForm,MotorForm
from flask import render_template,url_for, redirect
from flask_login import login_user, logout_user, current_user, login_required



@aplication.route('/')
def homePage():
    return render_template('index.html')

@aplication.route('/home/')
@login_required
def home():
    return render_template('homeuser.html')

@aplication.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        if user:
            login_user(user, remember=True)
            return render_template('homeuser.html')
    return render_template('login.html', form = form)


@aplication.route('/logout/', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homePage'))

@aplication.route('/admin/perfil/')
@login_required
def adminperfil():
    return render_template('admin.html')



@aplication.route('/home/sobre/')
@login_required
def inforLogin():
    return render_template('info.html')

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

@aplication.route('/home/funcionamento/')
@login_required
def funcionamento():
    return render_template('funcionamento.html')


@aplication.route('/admin/')
def admin():
    return render_template('loginAdmin.html')

####################FORMULARIOS DE CADASTROS####################
@aplication.route('/usuario/cadastrar/', methods=['POST', 'GET'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('conta.html', form = form)

@aplication.route('/motor/cadastrar/', methods=['POST', 'GET'])
def createmoor():
    form = MotorForm()
    if form.validate_on_submit():
        form.save()

    return render_template('motor.html', form = form)



@aplication.route('/admin/cadastrar/', methods=['POST', 'GET'])
def createadm():
    form = AdminForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('adminperfil'))
    return render_template('admiconta.html', form = form)


@aplication.route('/meus-upgrades')
@login_required
def meus_upgrades():
    # Graças ao 'backref' que criamos (historico_motores), 
    # podemos aceder diretamente aos upgrades do utilizador
    lista_upgrades = current_user.historico_motores
    # Ou de forma explícita:
    # lista_upgrades = motorUpgradeModel.query.filter_by(user_id=current_user.id).order_by(motorUpgradeModel.data_upgrade.desc()).all()
    
    return render_template('upgrade.html', upgrades=lista_upgrades)
