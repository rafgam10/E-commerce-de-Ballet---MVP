from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.models.categoria_model import Categoria
from src.models.produto_model import Produto
from src.models.produto_variavel import Produto_Variavel
from src.models.repositories.carrinho_repository import CarrinhoRepository
from src.models.repositories.endereco_repository import Endereco_Repository
from src.models.repositories.pedidos_repository import PedidosRepository


store_bp = Blueprint("store", __name__)


def _produtos_ativos_query():
    return Produto.query.filter(Produto.ativo.is_(True))


@store_bp.get("/")
def home():
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    produtos = (
        _produtos_ativos_query().order_by(Produto.created_at.desc()).limit(8).all()
    )
    return render_template("store/home.html", categorias=categorias, produtos=produtos)


@store_bp.get("/produtos")
def produtos():
    query = _produtos_ativos_query()
    busca = request.args.get("q", "").strip()
    categoria_slug = request.args.get("categoria", "").strip()
    tamanho = request.args.get("tamanho", "").strip()
    cor = request.args.get("cor", "").strip()
    preco_min = request.args.get("preco_min", "").strip()
    preco_max = request.args.get("preco_max", "").strip()

    if busca:
        query = query.filter(Produto.nome.ilike(f"%{busca}%"))
    if categoria_slug:
        query = query.join(Categoria).filter(Categoria.slug == categoria_slug)
    if tamanho or cor:
        query = query.join(Produto_Variavel)
        if tamanho:
            query = query.filter(Produto_Variavel.tamanho == tamanho)
        if cor:
            query = query.filter(Produto_Variavel.cor.ilike(f"%{cor}%"))
    if preco_min:
        query = query.filter(Produto.price >= float(preco_min))
    if preco_max:
        query = query.filter(Produto.price <= float(preco_max))

    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    produtos_lista = query.distinct().order_by(Produto.nome.asc()).all()
    return render_template(
        "store/products.html",
        produtos=produtos_lista,
        categorias=categorias,
        filtros=request.args,
    )


@store_bp.get("/categorias/<slug>")
def produtos_por_categoria(slug):
    categoria = Categoria.query.filter_by(slug=slug).first_or_404()
    produtos_lista = (
        _produtos_ativos_query()
        .filter(Produto.categoria_id == categoria.id)
        .order_by(Produto.nome.asc())
        .all()
    )
    categorias = Categoria.query.order_by(Categoria.nome.asc()).all()
    return render_template(
        "store/products.html",
        produtos=produtos_lista,
        categorias=categorias,
        categoria_atual=categoria,
        filtros={"categoria": slug},
    )


@store_bp.get("/produtos/<slug>")
def detalhe_produto(slug):
    produto = _produtos_ativos_query().filter(Produto.slug == slug).first_or_404()
    return render_template("store/product_detail.html", produto=produto)


@store_bp.get("/carrinho")
@login_required
def carrinho():
    resumo = CarrinhoRepository().resumir_carrinho(current_user.id)
    return render_template("store/cart.html", **resumo)


@store_bp.post("/carrinho/adicionar")
@login_required
def adicionar_carrinho():
    try:
        produto_variavel_id = int(request.form["produto_variavel_id"])
        quantidade = int(request.form.get("quantidade", 1))
        CarrinhoRepository().adicionar_produto_carrinho(
            current_user.id,
            produto_variavel_id,
            quantidade,
        )
        flash("Produto adicionado ao carrinho.", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(request.referrer or url_for("store.produtos"))


@store_bp.post("/carrinho/item/<int:item_id>/atualizar")
@login_required
def atualizar_item_carrinho(item_id):
    try:
        quantidade = int(request.form.get("quantidade", 1))
        CarrinhoRepository().atualizar_quantidade(current_user.id, item_id, quantidade)
        flash("Carrinho atualizado.", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("store.carrinho"))


@store_bp.post("/carrinho/item/<int:item_id>/remover")
@login_required
def remover_item_carrinho(item_id):
    try:
        CarrinhoRepository().remover_produto_do_carrinho(current_user.id, item_id)
        flash("Item removido do carrinho.", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("store.carrinho"))


@store_bp.get("/checkout")
@login_required
def checkout():
    resumo = CarrinhoRepository().resumir_carrinho(current_user.id)
    enderecos = Endereco_Repository().listar_endereco(current_user.id)
    return render_template("store/checkout.html", **resumo, enderecos=enderecos)


@store_bp.post("/checkout/endereco")
@login_required
def criar_endereco_checkout():
    try:
        Endereco_Repository().cadastrar_endereco(
            rua=request.form["rua"],
            numero=int(request.form["numero"]),
            cidade=request.form["cidade"],
            estado=request.form["estado"],
            cep=request.form["cep"],
            user_id=current_user.id,
            pais=request.form.get("pais") or "Brasil",
        )
        flash("Endereço cadastrado.", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("store.checkout"))


@store_bp.post("/checkout/confirmar")
@login_required
def confirmar_checkout():
    try:
        endereco_id = int(request.form["endereco_id"])
        pedido = PedidosRepository().criar_pedido_do_carrinho(
            current_user.id, endereco_id
        )
        flash("Pedido realizado com sucesso.", "success")
        return redirect(url_for("store.detalhe_pedido", pedido_id=pedido.id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("store.checkout"))


@store_bp.get("/pedidos")
@login_required
def pedidos():
    pedidos_lista = PedidosRepository().lista_pedidos(current_user.id)
    return render_template("store/orders.html", pedidos=pedidos_lista)


@store_bp.get("/pedidos/<int:pedido_id>")
@login_required
def detalhe_pedido(pedido_id):
    pedido = PedidosRepository().detalhe_pedido(pedido_id, current_user.id)
    if not pedido:
        flash("Pedido não encontrado.", "danger")
        return redirect(url_for("store.pedidos"))

    return render_template("store/order_detail.html", pedido=pedido)
