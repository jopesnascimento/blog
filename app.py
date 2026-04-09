from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-isso-em-producao")

# ─── Credenciais do dono ──────────────────────────────────────────────────────
# Defina ADMIN_USER e ADMIN_PASS como variáveis de ambiente no Render
ADMIN_USER = os.environ.get("ADMIN_USER", "joao")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "1234")

# ─── Conexão com MongoDB ──────────────────────────────────────────────────────
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client    = MongoClient(MONGO_URI)
db        = client["blog"]
colecao   = db["posts"]


# ─── Helpers de autenticação ──────────────────────────────────────────────────
def usuario_logado():
    return session.get("logado") is True

def requer_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not usuario_logado():
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ─── Helpers de posts ─────────────────────────────────────────────────────────
def validar_post(titulo, conteudo, autor):
    erros = []
    if not titulo.strip():
        erros.append("Título não pode estar vazio.")
    elif len(titulo.strip()) > 120:
        erros.append("Título muito longo (máx. 120 caracteres).")
    if not conteudo.strip():
        erros.append("Conteúdo não pode estar vazio.")
    if not autor.strip():
        erros.append("Autor não pode estar vazio.")
    elif len(autor.strip()) > 60:
        erros.append("Nome do autor muito longo (máx. 60 caracteres).")
    return erros

def buscar_post(post_id):
    try:
        post = colecao.find_one({"_id": ObjectId(post_id)})
    except InvalidId:
        return None, ("ID inválido", 400)
    if not post:
        return None, ("Post não encontrado", 404)
    return post, None


# ─── Rotas públicas ───────────────────────────────────────────────────────────
@app.route("/")
def home_page():
    posts = list(colecao.find().sort("_id", -1))
    return render_template("index.html", posts=posts, logado=usuario_logado())


@app.route("/post/<post_id>")
def post_detalhes(post_id):
    post, erro = buscar_post(post_id)
    if erro:
        return erro
    return render_template("post.html", post=post, logado=usuario_logado())


# ─── Login / Logout ───────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        user = request.form.get("usuario", "")
        pwd  = request.form.get("senha", "")
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session["logado"] = True
            return redirect("/")
        erro = "Usuário ou senha incorretos."
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ─── Rotas protegidas ─────────────────────────────────────────────────────────
@app.route("/novo")
@requer_login
def novo_post():
    return render_template("novo.html")

@app.route("/criar", methods=["POST"])
@requer_login
def criar_post():
    titulo   = request.form.get("titulo", "")
    conteudo = request.form.get("conteudo", "")
    autor    = request.form.get("autor", "")

    erros = validar_post(titulo, conteudo, autor)
    if erros:
        return render_template("novo.html", erros=erros,
                               titulo=titulo, conteudo=conteudo, autor=autor)

    colecao.insert_one({
        "titulo":   titulo.strip(),
        "conteudo": conteudo.strip(),
        "autor":    autor.strip(),
        "data":     datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    return redirect("/")

@app.route("/editar/<post_id>")
@requer_login
def editar_post(post_id):
    post, erro = buscar_post(post_id)
    if erro:
        return erro
    return render_template("editar.html", post=post)

@app.route("/atualizar/<post_id>", methods=["POST"])
@requer_login
def atualizar_post(post_id):
    post, erro = buscar_post(post_id)
    if erro:
        return erro

    titulo   = request.form.get("titulo", "")
    conteudo = request.form.get("conteudo", "")
    autor    = request.form.get("autor", "")

    erros = validar_post(titulo, conteudo, autor)
    if erros:
        post.update({"titulo": titulo, "conteudo": conteudo, "autor": autor})
        return render_template("editar.html", post=post, erros=erros)

    colecao.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {
            "titulo":   titulo.strip(),
            "conteudo": conteudo.strip(),
            "autor":    autor.strip(),
        }}
    )
    return redirect(f"/post/{post_id}")

@app.route("/deletar/<post_id>", methods=["POST"])
@requer_login
def deletar_post(post_id):
    post, erro = buscar_post(post_id)
    if erro:
        return erro
    colecao.delete_one({"_id": ObjectId(post_id)})
    return redirect("/")


# ─── Inicialização ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)