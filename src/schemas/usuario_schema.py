from pydantic import BaseModel


class UsuariosValidator(BaseModel):
    nome: str
    email: str
    senha: str
