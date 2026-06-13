from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required, logout_user


admin_bp = Blueprint("admin_api", __name__, url_prefix="/admin")


@admin_bp.get("/login")
def admin_login():
    if current_user.is_authenticated and current_user.role == "admin":
        return redirect(url_for("admin.index"))

    if current_user.is_authenticated:
        flash("Acesso restrito a administradores.", "danger")
        return redirect(url_for("store.home"))

    return redirect(url_for("auth.login", next=url_for("admin.index")))


@admin_bp.post("/logout")
@login_required
def admin_logout():
    logout_user()
    flash("Você saiu do painel administrativo.", "success")
    return redirect(url_for("store.home"))
