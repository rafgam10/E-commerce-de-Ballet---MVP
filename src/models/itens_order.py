from src.settings.extensions import db

class Itens_Order(db.Model):
    
    __tablename__ = 'itens_ordens'
    
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    
    ordens_id = db.Column(db.Integer, db.ForeignKey('ordens.id'), nullable=False)
    produto_variavel_id = db.Column(db.Integer, db.ForeignKey('variavel_produtos.id'), nullable=False)
    
    def __init__(self, ordens_id, produto_variavel_id, quantidade, preco):
        self.ordens_id = ordens_id
        self.produto_variavel_id = produto_variavel_id
        self.quantidade = quantidade
        self.preco = preco