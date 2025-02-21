from flask_sqlalchemy import SQLAlchemy

# Inicialização do banco de dados
db = SQLAlchemy()

# Modelo do Banco de Dados para Usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, senha):
        from werkzeug.security import generate_password_hash
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.senha_hash, senha)

# Modelo do Banco de Dados para Atividades
class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    horas = db.Column(db.Integer, nullable=False)
    horas_aproveitadas = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    user = db.relationship('Usuario', backref=db.backref('atividades', lazy=True))
