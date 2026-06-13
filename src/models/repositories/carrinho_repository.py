from src.settings.extensions import db

from src.models.interfaces.carrinho_interface import ICarrinho

from src.models.carrinho_model import Carrinhos, CartStatus
from src.models.itens_carrinho import Itens_Carrinho
from src.models.produto_variavel import Produto_Variavel
from datetime import datetime, timedelta, timezone


class CarrinhoRepository(ICarrinho):

    def obter_ou_criar_carrinho_ativo(self, id_user: int) -> Carrinhos:
        carrinho = (
            db.session.query(Carrinhos)
            .filter(
                Carrinhos.user_id == id_user,
                Carrinhos.status == CartStatus.ATIVO.value,
            )
            .first()
        )

        if carrinho:
            return carrinho

        carrinho = Carrinhos(id_user)
        db.session.add(carrinho)
        db.session.flush()
        return carrinho

    def adicionar_produto_carrinho(
        self, id_user: int, produto_variavel_id: int, quantidade: int
    ):
        if quantidade <= 0:
            raise Exception("Quantidade deve ser maior que zero")

        variacao = db.session.get(Produto_Variavel, produto_variavel_id)
        if not variacao:
            raise Exception("Variação do produto não encontrada")

        if not variacao.variaveis.ativo:
            raise Exception("Produto indisponível")

        carrinho = self.obter_ou_criar_carrinho_ativo(id_user)
        item = (
            db.session.query(Itens_Carrinho)
            .filter(
                Itens_Carrinho.carrinho_id == carrinho.id,
                Itens_Carrinho.produto_variavel_id == produto_variavel_id,
            )
            .first()
        )

        quantidade_final = quantidade + (item.quantidade if item else 0)
        if quantidade_final > variacao.estoque:
            raise Exception("Estoque insuficiente")

        if item:
            item.quantidade = quantidade_final
        else:
            item = Itens_Carrinho(
                quantidade=quantidade,
                carrinho_id=carrinho.id,
                produto_variavel_id=produto_variavel_id,
            )
            db.session.add(item)

        db.session.commit()
        return item

    def remover_produto_do_carrinho(self, id_user: int, item_id: int):
        carrinho = self.visualizar_carrinho_ativo(id_user)
        if not carrinho:
            raise Exception("Carrinho não encontrado")

        item = (
            db.session.query(Itens_Carrinho)
            .filter(
                Itens_Carrinho.id == item_id,
                Itens_Carrinho.carrinho_id == carrinho.id,
            )
            .first()
        )
        if not item:
            raise Exception("Item não encontrado no carrinho")

        db.session.delete(item)
        db.session.commit()
        return item

    def atualizar_quantidade(self, id_user: int, item_id: int, quantidade: int):
        if quantidade <= 0:
            return self.remover_produto_do_carrinho(id_user, item_id)

        carrinho = self.visualizar_carrinho_ativo(id_user)
        if not carrinho:
            raise Exception("Carrinho não encontrado")

        item = (
            db.session.query(Itens_Carrinho)
            .filter(
                Itens_Carrinho.id == item_id,
                Itens_Carrinho.carrinho_id == carrinho.id,
            )
            .first()
        )
        if not item:
            raise Exception("Item não encontrado no carrinho")

        if quantidade > item.variavel_produtos.estoque:
            raise Exception("Estoque insuficiente")

        item.quantidade = quantidade
        db.session.commit()
        return item

    def visualizar_carrinho_ativo(self, id_user: int):
        return (
            db.session.query(Carrinhos)
            .filter(
                Carrinhos.user_id == id_user,
                Carrinhos.status == CartStatus.ATIVO.value,
            )
            .first()
        )

    def analisar_abandono_carrinho(self, horas: int = 24):
        agora = datetime.now(timezone.utc).replace(tzinfo=None)
        limite = agora - timedelta(hours=horas)
        return (
            db.session.query(Carrinhos)
            .filter(
                Carrinhos.status == CartStatus.ATIVO.value,
                Carrinhos.created_at <= limite,
            )
            .all()
        )

    def calcular_total(self, carrinho: Carrinhos) -> float:
        if not carrinho:
            return 0

        return sum(
            item.quantidade * item.variavel_produtos.variaveis.price
            for item in carrinho.itens_carrinhos
        )

    def resumir_carrinho(self, id_user: int) -> dict:
        carrinho = self.visualizar_carrinho_ativo(id_user)
        itens = carrinho.itens_carrinhos if carrinho else []
        return {
            "carrinho": carrinho,
            "itens": itens,
            "total": self.calcular_total(carrinho),
            "quantidade_itens": sum(item.quantidade for item in itens),
        }
