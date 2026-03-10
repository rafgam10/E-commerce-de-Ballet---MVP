from src.settings.extensions import db

class Produto_Images(db.Model):
    
    __tablename__="imagens_produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)