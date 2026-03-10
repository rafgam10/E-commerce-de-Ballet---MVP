from src.settings.extensions import db
from enum import Enum

class Pais(Enum):
    BRASIL = "Brasil"
    ESTADOS_UNIDOS = "Estados Unidos"
    CANADA = "Canadá"
    PORTUGAL = "Portugal"
    JAPAO = "Japão"
    ALEMANHA = "Alemanha"


class Endereco(db.Model):
    
    __tablename__="enderecos"
    
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    pais = db.Column(db.String(255), default=Pais.BRASIL.value, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    ordens = db.relationship(
        'Ordens',
        backref='enderecos',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __init__(self, rua, numero, cidade, estado, cep, pais):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.pais = pais
        
    def __repr__(self):
        return f"Endereco: {self.rua} - {self.numero} - {self.pais} - {self.user_id}"