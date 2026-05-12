from abc import ABC, abstractmethod

class ICarrinho(ABC):
    
    @abstractmethod
    def visualizar_carrinho_ativo(): pass
    
    @abstractmethod
    def analisar_abandono_carrinho(): pass
    