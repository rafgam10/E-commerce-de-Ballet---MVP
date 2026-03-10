from src.settings.extensions import db
from enum import Enum
from datetime import datetime


class Status(Enum):
    PROCESSADO = 'processado'
    PAGO = 'pago'
    ENVIADO = 'enviado'


class Ordens(db.Model):
    
    __tablename__ = 'ordens'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default=Status.PROCESSADO.value, nullable=False)
    preco_total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos.id'), nullable=False)
    
    itens_ordens = db.relationship(
        'Itens_Order',
        backref='ordens',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __init__(self, user_id, endereco_id, status, preco_total):
        self.user_id = user_id
        self.endereco_id = endereco_id
        self.status = status
        self.preco_total = preco_total
        
    def __repr__(self):
        return f"Ordens: {self.user_id} - {self.endereco_id} - {self.status} - {self.preco_total}"