from src.settings.extensions import db
from datetime import datetime
from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    CLIENTE = 'cliente'


class Usuario(db.Model):
    
    __tablename__="usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default=Role.CLIENTE)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    enderecos = db.relationship('Endereco', backref="usuarios")
    
    
    def __init__(self, nome, email, senha, role):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.role = role
    
    def __repr__(self):
        return f"Usuario: {self.nome} - {self.email} - {self.role} - {self.created_at}"
    
    def __to_dict__(self):
        ...