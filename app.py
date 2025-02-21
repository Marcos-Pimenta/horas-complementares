from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import json
import os

# Carregar variáveis do .env
load_dotenv()

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "sua_chave_secreta")

# Banco de Dados
db = SQLAlchemy()
migrate = Migrate()

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    atividades = db.relationship('Atividade', backref='usuario', lazy=True)

    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

# Modelo de Atividades
class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    horas = db.Column(db.Integer, nullable=False)
    horas_aproveitadas = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Inicializar banco no app
db.init_app(app)
migrate.init_app(app, db)

# Criar banco no contexto do Flask
with app.app_context():
    db.create_all()
    print("✅ Banco de dados conectado e tabelas criadas!")

# Tabela de Limites
LIMITES_TIPO = {
    "Projeto de Extensão": (40, 10),
    "Atividades Culturais": (5, 80),
    "Visitas Técnicas": (40, 100),
    "Visitas a Feiras e Exposições": (5, 20),
    "Cursos de Idiomas": (20, 60),
    "Palestras como Ouvinte": (10, 80),
    "Palestras como Apresentador": (15, 100),
    "Projeto Empresa Júnior": (20, 20),
    "Monitoria Acadêmica": (40, 70),
    "Iniciação Científica": (40, 80),
    "Publicação de Artigos": (10, 100),
    "Registro de Patentes": (40, 100),
    "Premiação Resultante": (10, 100),
    "Colaborador em Congressos": (10, 100),
}

# Rota inicial
@app.route('/')
def index():
    if not session.get("user_id"):
        flash("Você precisa estar logado para acessar esta página.", "warning")
        return redirect(url_for('login'))

    user_id = session.get("user_id")
    atividades = Atividade.query.filter_by(user_id=user_id).all()
    return render_template('index.html', atividades=atividades, tipos=list(LIMITES_TIPO.keys()))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        user = Usuario.query.filter_by(username=username).first()
        
        if not user or not user.check_password(senha):
            flash("Usuário ou senha inválidos!", "danger")
            return redirect(url_for('login'))
        
        session['user_id'] = user.id
        session['username'] = user.username
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for('index'))
    
    return render_template('login.html')

# Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        
        if Usuario.query.filter_by(username=username).first():
            flash("Usuário já existe!", "danger")
            return render_template('cadastro.html')

        novo_usuario = Usuario(username=username)
        novo_usuario.set_password(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça o login.", "success")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for('login'))

# Adicionar atividade
@app.route('/adicionar', methods=['POST'])
def adicionar():
    try:
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        tipo = request.form['tipo']
        horas = int(request.form['horas'])

        if tipo not in LIMITES_TIPO:
            raise ValueError("Tipo de atividade inválido.")

        limite_tipo, aproveitamento = LIMITES_TIPO[tipo]
        horas_aproveitadas = round(horas * (aproveitamento / 100), 2)

        total_horas_tipo = db.session.query(db.func.sum(Atividade.horas_aproveitadas)) \
            .filter(Atividade.tipo == tipo, Atividade.user_id == session.get("user_id")).scalar() or 0

        if total_horas_tipo + horas_aproveitadas > limite_tipo:
            raise ValueError(f"Limite de horas excedido para '{tipo}'. Máximo permitido: {limite_tipo}.")

        nova_atividade = Atividade(
            descricao=descricao,
            categoria=categoria,
            tipo=tipo,
            horas=horas,
            horas_aproveitadas=horas_aproveitadas,
            user_id=session.get("user_id")
        )
        db.session.add(nova_atividade)
        db.session.commit()

        flash("Atividade adicionada com sucesso!", "success")
        return redirect(url_for('index'))
    
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('index'))

# Relatório
@app.route('/relatorio')
def relatorio():
    user_id = session.get("user_id")

    total_extensao = db.session.query(db.func.sum(Atividade.horas_aproveitadas)) \
        .filter(Atividade.categoria == "Extensão", Atividade.user_id == user_id).scalar()
    total_extensao = round(total_extensao if total_extensao is not None else 0, 2)

    total_ensino = db.session.query(db.func.sum(Atividade.horas_aproveitadas)) \
        .filter(Atividade.categoria == "Ensino", Atividade.user_id == user_id).scalar()
    total_ensino = round(total_ensino if total_ensino is not None else 0, 2)

    total_pesquisa = db.session.query(db.func.sum(Atividade.horas_aproveitadas)) \
        .filter(Atividade.categoria == "Pesquisa", Atividade.user_id == user_id).scalar()
    total_pesquisa = round(total_pesquisa if total_pesquisa is not None else 0, 2)

    # 🔴  DEPURAÇÃO
    print(f"Total Extensão: {total_extensao} | Total Ensino: {total_ensino} | Total Pesquisa: {total_pesquisa}")

    resumo_tipo = {
        tipo: round((db.session.query(db.func.sum(Atividade.horas_aproveitadas))
                     .filter(Atividade.tipo == tipo, Atividade.user_id == user_id)
                     .scalar() or 0), 2)
        for tipo in LIMITES_TIPO.keys()
    }

    return render_template('relatorio.html',
                           total_extensao=total_extensao,
                           total_ensino=total_ensino,
                           total_pesquisa=total_pesquisa,
                           resumo_tipo=resumo_tipo)



@app.route('/apagar_tudo', methods=['POST'])
def apagar_tudo():
    if not session.get("user_id"):
        flash("Você precisa estar logado para apagar atividades!", "danger")
        return redirect(url_for('login'))
    
    db.session.query(Atividade).filter_by(user_id=session.get("user_id")).delete()
    db.session.commit()
    
    flash("Todas as atividades foram apagadas!", "info")
    return redirect(url_for('index'))

# Rodar o app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
