from src.settings.extensions import db
from src.models.produto_image import public_image_url
from datetime import datetime, timezone


class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)

    variates = db.relationship(
        "Produto_Variavel", backref="variaveis", lazy=True, cascade="all, delete-orphan"
    )

    images = db.relationship(
        "Produto_Images", backref="produto", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, nome, slug, descricao, price, ativo, categoria_id):
        self.nome = nome
        self.slug = slug
        self.descricao = descricao
        self.price = price
        self.ativo = ativo
        self.categoria_id = categoria_id

    def __repr__(self):
        return self.nome

    def imagem_principal(self):
        for image in self.images:
            image_url = public_image_url(image.image_url)
            if image_url:
                return image_url
        return None
