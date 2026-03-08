from src.settings.extensions import db
from datetime import datetime
from enum import Enum


class Produto(db.Model):
    
    __tablename__="produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    
    