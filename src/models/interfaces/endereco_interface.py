from abc import ABC, abstractmethod


class IEndereco(ABC):

    @abstractmethod
    def cadastrar_endereco(self) -> None:
        pass

    @abstractmethod
    def editar_endereco(self) -> None:
        pass

    @abstractmethod
    def listar_endereco(self) -> None:
        pass

    @abstractmethod
    def remover_endereco(self) -> None:
        pass
