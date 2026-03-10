from src.settings.extensions import db

class Produto_Variavel(db.Model):
    
    __tablename__="variavel_produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    tamanho = db.Column(db.String(10), nullable=False)
    cor = db.Column(db.String(100), nullable=False)
    estoque = db.Column(db.Integer, default=0, nullable=False)
    sku = db.Column(db.String(100), nullable=False)
    
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    
    itens_carrinho = db.relationship(
        'Itens_Carrinho',
        backref='variavel_produtos',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    itens_ordens = db.relationship(
        'Itens_Order',
        backref='variavel_produtos',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __init__(self, tamanho, cor, estoque, sku, produto_id):
        self.tamanho = tamanho
        self.cor = cor
        self.estoque = estoque
        self.sku = sku
        self.produto_id = produto_id
        
    def __repr__(self):
        return f"Produto_Variavel: {self.tamanho} - {self.cor} - {self.tamanho}"