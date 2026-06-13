from src.settings.extensions import db
from src.models.interfaces.pedidos_interface import IPedidos

from src.models.ordens import Ordens, Status
from src.models.itens_order import Itens_Order
from src.models.endereco_model import Endereco
from src.models.carrinho_model import CartStatus
from src.models.repositories.carrinho_repository import CarrinhoRepository


class PedidosRepository(IPedidos):

    def lista_pedidos(self, user_id: int = None) -> list[Ordens]:
        try:
            query = db.session.query(Ordens).order_by(Ordens.created_at.desc())
            if user_id is not None:
                query = query.filter(Ordens.user_id == user_id)
            lista_pedidos = query.all()
            return lista_pedidos
        except Exception as e:
            db.session.rollback()
            return str(e)

    def detalhe_pedido(self, id: int, user_id: int = None) -> Ordens:
        try:
            query = db.session.query(Ordens).filter(Ordens.id == id)
            if user_id is not None:
                query = query.filter(Ordens.user_id == user_id)
            pedido_detalhe = query.first()
            if not pedido_detalhe:
                return None

            return pedido_detalhe
        except Exception as e:
            db.session.rollback()
            return str(e)

    def atualizar_status(self, id: int, status: Status) -> Ordens:
        try:
            select_pedido = db.session.get(Ordens, id)
            if not select_pedido:
                raise Exception("Pedido não encontrado")

            status_value = status.value if isinstance(status, Status) else status
            status_validos = {item.value for item in Status}
            if status_value not in status_validos:
                raise Exception("Status inválido")

            select_pedido.status = status_value
            db.session.commit()
            return select_pedido
        except Exception as e:
            db.session.rollback()
            return str(e)

    def criar_pedido_do_carrinho(self, user_id: int, endereco_id: int) -> Ordens:
        try:
            endereco = (
                db.session.query(Endereco)
                .filter(
                    Endereco.id == endereco_id,
                    Endereco.user_id == user_id,
                )
                .first()
            )
            if not endereco:
                raise Exception("Endereço não encontrado")

            carrinho_repo = CarrinhoRepository()
            carrinho = carrinho_repo.visualizar_carrinho_ativo(user_id)
            if not carrinho or not carrinho.itens_carrinhos:
                raise Exception("Carrinho vazio")

            preco_total = 0
            for item in carrinho.itens_carrinhos:
                variacao = item.variavel_produtos
                if item.quantidade > variacao.estoque:
                    raise Exception(f"Estoque insuficiente para {variacao.sku}")
                preco_total += item.quantidade * variacao.variaveis.price

            pedido = Ordens(
                user_id=user_id,
                endereco_id=endereco_id,
                preco_total=preco_total,
            )
            db.session.add(pedido)
            db.session.flush()

            for item in carrinho.itens_carrinhos:
                variacao = item.variavel_produtos
                produto = variacao.variaveis
                variacao.estoque -= item.quantidade
                db.session.add(
                    Itens_Order(
                        ordens_id=pedido.id,
                        produto_variavel_id=variacao.id,
                        quantidade=item.quantidade,
                        preco=produto.price,
                        nome_produto=produto.nome,
                        sku=variacao.sku,
                        tamanho=variacao.tamanho,
                        cor=variacao.cor,
                    )
                )

            carrinho.status = CartStatus.CONVERTIDO.value
            db.session.commit()
            return pedido
        except Exception:
            db.session.rollback()
            raise

    def acessar_itens_de_pedidos(self, pedido_id: int):
        return (
            db.session.query(Itens_Order)
            .filter(Itens_Order.ordens_id == pedido_id)
            .all()
        )

    def ver_total_compra(self, pedido_id: int):
        pedido = db.session.get(Ordens, pedido_id)
        return pedido.preco_total if pedido else 0
