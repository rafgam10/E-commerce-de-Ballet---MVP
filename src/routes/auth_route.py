from flask import Blueprint, request, jsonify, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from urllib.parse import urlsplit

from src.controllers.auth_controller import AuthController
from src.models.usuario_model import Usuario
from src.settings.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
controller = AuthController()


def destino_seguro_pos_login(default):
    next_url = request.args.get("next")
    if not next_url:
        return default

    parsed = urlsplit(next_url)
    if parsed.path == "/admin/login":
        return url_for("admin.index")

    if parsed.netloc and parsed.netloc != request.host:
        return default

    return parsed.path or default


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    try:
        data = (
            request.get_json(silent=True) if request.is_json else request.form.to_dict()
        )
        response = controller.login(data)

        if request.is_json:
            return jsonify(response), 200

        usuario = db.session.get(Usuario, response["usuario"]["id"])
        login_user(usuario)
        flash("Login realizado com sucesso.", "success")
        return redirect(destino_seguro_pos_login(url_for("store.home")))

    except Exception as e:
        if request.is_json:
            return jsonify({"msg": str(e)}), 400

        flash(str(e), "danger")
        return render_template("auth/login.html"), 400


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "success")

    if request.is_json:
        return jsonify({"msg": "Logout realizado com sucesso"}), 200

    return redirect(url_for("store.home"))


@auth_bp.route("/register", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "GET":
        return render_template("auth/register.html")

    try:
        data = (
            request.get_json(silent=True) if request.is_json else request.form.to_dict()
        )

        usuario_response = controller.cadastro_usuario_cliente(data)

        if request.is_json:
            return (
                jsonify(
                    {
                        "msg": "Usuário criado com sucesso.",
                        **usuario_response,
                    }
                ),
                201,
            )

        usuario = db.session.get(Usuario, usuario_response["usuario"]["id"])
        login_user(usuario)
        flash("Cadastro realizado com sucesso.", "success")
        return redirect(url_for("store.home"))

    except Exception as e:
        if request.is_json:
            return jsonify({"msg": str(e)}), 400

        flash(str(e), "danger")
        return render_template("auth/register.html"), 400
