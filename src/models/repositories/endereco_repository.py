import re

from src.settings.extensions import db
from src.models.endereco_model import Endereco
from src.models.interfaces.endereco_interface import IEndereco


def normalizar_cep(cep: str) -> str:
    numeros = re.sub(r"\D", "", cep or "")
    if len(numeros) != 8:
        raise Exception("CEP inválido. Use o formato 00000-000.")

    return f"{numeros[:5]}-{numeros[5:]}"


class Endereco_Repository(IEndereco):

    def listar_endereco(self, user_id: int = None):
        query = db.session.query(Endereco)
        if user_id is not None:
            query = query.filter(Endereco.user_id == user_id)
        lista_endereco = query.all()
        return [e._to_dict() for e in lista_endereco]

    def cadastrar_endereco(
        self,
        rua: str,
        numero: int,
        cidade: str,
        estado: str,
        cep: str,
        user_id: int,
        pais="Brasil",
    ):
        cep = normalizar_cep(cep)
        novo_endereco = Endereco(
            rua,
            numero,
            cidade,
            estado,
            cep,
            user_id,
            pais,
        )

        db.session.add(novo_endereco)
        db.session.commit()
        return novo_endereco

    def editar_endereco(self, id_endereco, data: dict):
        endereco = db.session.get(Endereco, id_endereco)
        if not endereco:
            raise Exception("Endereço não encontrado")

        if "cep" in data and data["cep"] is not None:
            data["cep"] = normalizar_cep(data["cep"])

        for campo in ("rua", "numero", "cidade", "estado", "cep", "pais"):
            if campo in data and data[campo] is not None:
                setattr(endereco, campo, data[campo])

        db.session.commit()
        return endereco

    def remover_endereco(self, id_endereco):
        endereco = db.session.get(Endereco, id_endereco)
        if not endereco:
            raise Exception("Endereço não encontrado")

        db.session.delete(endereco)
        db.session.commit()
        return endereco
