from src.settings.extensions import db

class Itens_Carrinho(db.Model):
    
    __tablename__ = "itens_carrinho"
    
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinhos.id'), nullable=False)
    produto_variavel_id = db.Column(db.Integer, db.ForeignKey('variavel_produtos.id'), nullable=False)