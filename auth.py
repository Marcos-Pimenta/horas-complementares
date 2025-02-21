from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario

auth_bp = Blueprint('auth', __name__)

# Rota de cadastro
@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Validação de campos
        if not username or not password:
            flash("Preencha todos os campos!", "danger")
            return render_template('cadastro.html', error="Preencha todos os campos.")

        if Usuario.query.filter_by(username=username).first():
            flash("Usuário já existe!", "danger")
            return render_template('cadastro.html', error="Usuário já existe!")

        # Criar novo usuário
        novo_usuario = Usuario(username=username)
        novo_usuario.set_password(password)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça o login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('cadastro.html')

# Rota de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        usuario = Usuario.query.filter_by(username=username).first()

        # Validação de credenciais
        if not usuario or not usuario.check_password(password):
            flash("Usuário ou senha inválidos.", "danger")
            return render_template('login.html', error="Usuário ou senha inválidos.")

        # Login bem-sucedido
        session['user_id'] = usuario.id
        session['username'] = usuario.username
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('index'))

    return render_template('login.html')

# Rota de logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for('auth.login'))
