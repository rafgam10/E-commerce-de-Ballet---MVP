from pathlib import Path

from src.settings.extensions import db
from flask import current_app, has_app_context, has_request_context, url_for


def public_image_url(value):
    if not value:
        return None
    if value.startswith(("http://", "https://", "/")):
        return value

    if has_app_context():
        image_path = Path(current_app.config["UPLOAD_FOLDER"]) / value
        if not image_path.exists():
            return None

    if has_request_context():
        return url_for("uploaded_file", filename=value)
    return f"/uploads/{value}"


class Produto_Images(db.Model):

    __tablename__ = "imagens_produtos"

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)

    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)

    @property
    def url(self):
        return public_image_url(self.image_url)
