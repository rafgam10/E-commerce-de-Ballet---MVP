from abc import ABC, abstractmethod

class UsuarioInterface(ABC):
    
    @abstractmethod
    def criar_usuario(self) -> None: pass
    
    @abstractmethod
    def recuperar_senha(self) -> None: pass
    
    @abstractmethod
    def get_usuario(self) -> None: pass
    
    @abstractmethod
    def get_all_usuarios(self) -> None: pass
    
    @abstractmethod
    def get_admin(self) -> None: pass
    
    @abstractmethod
    def get_all_admin(self) -> None: pass
    
    @abstractmethod
    def atualizar_usuario(self) -> None: pass