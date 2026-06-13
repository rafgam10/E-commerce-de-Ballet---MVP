from src.services.auth_services import AuthService


class AuthController:

    @staticmethod
    def login(data):
        if not data or not data.get("email") or not data.get("senha"):
            raise Exception("E-mail e senha são obrigatórios")

        response = AuthService.login(data["email"], data["senha"])

        return response

    @staticmethod
    def cadastro_usuario_cliente(data):
        if not data:
            raise Exception("Dados de cadastro são obrigatórios")
        if not data.get("nome") or not data.get("email") or not data.get("senha"):
            raise Exception("Nome, e-mail e senha são obrigatórios")
        if len(data["senha"]) < 6:
            raise Exception("A senha deve ter pelo menos 6 caracteres")

        response = AuthService.cadastro(data["nome"], data["email"], data["senha"])

        return response
