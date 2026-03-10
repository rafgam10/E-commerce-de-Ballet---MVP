from src.settings.extensions import db
from datetime import datetime

class Carrinhos(db.Model):
    
    __tablename__ = "carrinhos"
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    itens_carrinhos = db.relationship(
        'Itens_Carrinho',
        backref='carrinhos',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __init__(self, user_id):
        self.user_id = user_id
        
    def __repr__(self):
        return f"Carrinhos: {self.id} - {self.user_id}"