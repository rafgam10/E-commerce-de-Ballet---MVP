from src.settings.extensions import db


class Itens_Order(db.Model):

    __tablename__ = "itens_ordens"

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    nome_produto = db.Column(db.String(255), nullable=True)
    sku = db.Column(db.String(100), nullable=True)
    tamanho = db.Column(db.String(10), nullable=True)
    cor = db.Column(db.String(100), nullable=True)

    ordens_id = db.Column(db.Integer, db.ForeignKey("ordens.id"), nullable=False)
    produto_variavel_id = db.Column(
        db.Integer, db.ForeignKey("variavel_produtos.id"), nullable=False
    )

    def __init__(
        self,
        ordens_id,
        produto_variavel_id,
        quantidade,
        preco,
        nome_produto=None,
        sku=None,
        tamanho=None,
        cor=None,
    ):
        self.ordens_id = ordens_id
        self.produto_variavel_id = produto_variavel_id
        self.quantidade = quantidade
        self.preco = preco
        self.nome_produto = nome_produto
        self.sku = sku
        self.tamanho = tamanho
        self.cor = cor
