from src.settings.extensions import db
from datetime import datetime, timezone
from enum import Enum


class CartStatus(Enum):
    ATIVO = "ativo"
    CONVERTIDO = "convertido"


class Carrinhos(db.Model):

    __tablename__ = "carrinhos"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
    status = db.Column(db.String(20), default=CartStatus.ATIVO.value, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    itens_carrinhos = db.relationship(
        "Itens_Carrinho", backref="carrinhos", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, user_id):
        self.user_id = user_id
        self.status = CartStatus.ATIVO.value

    def __repr__(self):
        return f"Carrinhos: {self.id} - {self.user_id}"
