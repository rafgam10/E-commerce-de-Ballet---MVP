from src.services.auth_services import AuthService

class AuthController:
    

    @staticmethod
    def login(data):

        response = AuthService.login(
            data["email"],
            data["senha"]
        )

        return response
    
    @staticmethod
    def cadastro_usuario_cliente(data):
        
        response = AuthService.cadastro(
            data["nome"],
            data["email"],
            data["senha"]
        )

        return response
        
        
    