
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from backend.app.forms import LoginForm, RegisterForm
from backend.app.models import User
from backend.app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_url = request.args.get('next') or ( url_for('admin.dashboard') if user.is_admin else ( url_for('company.dashboard') if getattr(user,'company',None) else url_for('public.home') ) )
            return redirect(next_url)
        flash('Credenciais inválidas.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/cadastro', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.strip().lower()).first():
            flash('E-mail já cadastrado.', 'danger')
        else:
            u = User(name=form.name.data.strip(), email=form.email.data.strip().lower())
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            flash(f'Conta criada. Bem-vindo(a), {u.name}!', 'success')
            return redirect(url_for('public.home'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('public.home'))
