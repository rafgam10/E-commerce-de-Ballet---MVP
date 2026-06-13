import re
import unicodedata


def gerar_slug(texto):
    texto = (
        unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    )
    texto = re.sub(r"[^a-zA-Z0-9\s-]", "", texto)
    texto = texto.lower()
    texto = re.sub(r"\s+", "-", texto)
    return texto
