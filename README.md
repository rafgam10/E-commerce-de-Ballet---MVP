# E-commerce de Ballet - MVP

Loja completa em Flask/Jinja para venda de produtos de ballet. O fluxo principal cobre catálogo, variações, carrinho, checkout simulado, pedidos do cliente e painel administrativo.

## Funcionalidades

- Autenticação com cadastro, login, logout e senha com bcrypt.
- Loja Jinja responsiva com home, catálogo, detalhe de produto, carrinho, checkout e pedidos.
- Produtos com categoria, imagens, preço, status ativo/inativo e variações por tamanho/cor/estoque/SKU.
- Upload de imagens de produto pelo computador no painel administrativo.
- Carrinho persistente por usuário logado.
- Checkout com endereço e pagamento PIX/manual simulado.
- Pedido criado a partir do carrinho, com baixa de estoque e snapshot dos itens.
- Flask-Admin protegido para usuários admin.
- Seed de demonstração e comando para criar admin.
- Testes isolados em SQLite em memória.

## Setup Local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env` com seus segredos e banco. Para desenvolvimento simples, SQLite funciona bem.

```bash
flask --app run.py db upgrade
flask --app run.py seed-demo
flask --app run.py create-admin
python run.py
```

Acesse:

- Loja: `http://localhost:5000/`
- Admin: `http://localhost:5000/admin/`

## Variáveis De Ambiente

```env
SECRET_KEY=troque-essa-chave
JWT_SECRET_KEY=troque-essa-chave-jwt
SQLALCHEMY_DATABASE_URI=sqlite:///ballet.db
FLASK_DEBUG=1
```

Para MySQL:

```env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@localhost:3306/ballet_db
```

## Comandos Úteis

```bash
flask --app run.py db migrate -m "mensagem"
flask --app run.py db upgrade
flask --app run.py seed-demo
flask --app run.py create-admin
pytest -q
```

## Testes

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider
```

A suíte cobre auth, repositórios, catálogo, carrinho, checkout, pedido e proteção do admin.

## Deploy

Use Gunicorn em produção:

```bash
gunicorn "run:app" --bind "0.0.0.0:${PORT:-8000}"
```

Antes do deploy:

- Configure `SECRET_KEY`, `JWT_SECRET_KEY` e `SQLALCHEMY_DATABASE_URI` no ambiente da plataforma.
- Rode `flask --app run.py db upgrade`.
- Crie um admin com `flask --app run.py create-admin`.
- Evite usar armazenamento local de upload em plataformas com filesystem efêmero.

## Rotas Principais

- `/` home
- `/produtos` catálogo com busca/filtros
- `/produtos/<slug>` detalhe do produto
- `/categorias/<slug>` filtro por categoria
- `/carrinho` carrinho
- `/checkout` checkout
- `/pedidos` pedidos do cliente
- `/admin/` painel administrativo
- `/auth/login`, `/auth/register`, `/auth/logout`

## Imagens De Produto

No admin, acesse `Imagens` e escolha o produto. O campo `Imagem do produto` abre o seletor de arquivos do computador e salva a imagem em `uploads/products`. A loja exibe esses arquivos por `/uploads/products/<arquivo>`.

## Design

Referência inicial: https://stitch.withgoogle.com/projects/14858003210999483372?pli=1
