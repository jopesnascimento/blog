from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import os

app = Flask(__name__)

# ─── Conexão com MongoDB ───────────────────────────────────────────────────────
# Local:  mongodb://localhost:27017/
# Atlas:  mongodb+srv://usuario:senha@cluster.mongodb.net/blog
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["blog"]
colecao = db["posts"]


# ─── Helpers ──────────────────────────────────────────────────────────────────
def validar_post(titulo, conteudo, autor):
    """Retorna lista de erros. Lista vazia = tudo ok."""
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
    """Busca post pelo ID. Retorna (post, erro) — um dos dois será None."""
    try:
        post = colecao.find_one({"_id": ObjectId(post_id)})
    except InvalidId:
        return None, ("ID inválido", 400)
    if not post:
        return None, ("Post não encontrado", 404)
    return post, None


# ─── Rotas ────────────────────────────────────────────────────────────────────
@app.route("/")
def home_page():
    posts = list(colecao.find().sort("_id", -1))  # mais recentes primeiro
    return render_template("index.html", posts=posts)


@app.route("/post/<post_id>")
def post_detalhes(post_id):
    post, erro = buscar_post(post_id)
    if erro:
        return erro
    return render_template("post.html", post=post)


@app.route("/novo")
def novo_post():
    return render_template("novo.html")


@app.route("/criar", methods=["POST"])
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
def editar_post(post_id):
    post, erro = buscar_post(post_id)
    if erro:
        return erro
    return render_template("editar.html", post=post)


@app.route("/atualizar/<post_id>", methods=["POST"])
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