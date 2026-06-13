from src.models.interfaces.usuario_interface import UsuarioInterface


class UsuarioController:

    def __init__(self, usuario_repository: UsuarioInterface):
        self.__repo = usuario_repository

    # Métodos de Funcionalidades:
    def registrar_usuario(self, usuario_data: dict) -> None:
        self.__validar_dados_usuario(usuario_data)
        self.__repo.criar_usuario(**usuario_data)

    # Métodos Auxiliares:
    def __validar_dados_usuario(self, usuario_data: dict) -> None:

        email = usuario_data["email"]
        senha = usuario_data["senha"]

        if len(email) < 8 and len(email) > 200:
            raise Exception("Email invalida...")

        if len(senha) < 3 or not senha:
            raise Exception("Senha invalida...")
