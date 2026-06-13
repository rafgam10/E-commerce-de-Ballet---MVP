from abc import ABC, abstractmethod


class ICarrinho(ABC):

    @abstractmethod
    def adicionar_produto_carrinho(self):
        pass

    @abstractmethod
    def remover_produto_do_carrinho(self):
        pass

    @abstractmethod
    def atualizar_quantidade(self):
        pass

    @abstractmethod
    def visualizar_carrinho_ativo(self):
        pass

    @abstractmethod
    def analisar_abandono_carrinho():
        pass
