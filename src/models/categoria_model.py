from src.settings.extensions import db

class Categoria(db.Model):
    
    __tablename__="categorias"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    
    def __init__(self, nome, slug):
        self.nome = nome
        self.slug = slug
    
    def __repr__(self):
        return f"Categoria: {self.nome} - {self.slug}"