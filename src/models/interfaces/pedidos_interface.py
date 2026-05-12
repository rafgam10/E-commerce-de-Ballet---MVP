from abc import ABC, abstractmethod

class IPedidos(ABC):
    
    @abstractmethod
    def lista_pedidos() -> None: pass
    
    @abstractmethod
    def detalhe_pedido() -> None: pass
    
    @abstractmethod
    def atualizar_status() -> None: pass
    
    @abstractmethod
    def acessar_itens_de_pedidos() -> None: pass
    
    @abstractmethod
    def ver_total_compra() -> None: pass