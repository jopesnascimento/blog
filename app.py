from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from functools import wraps
import os
import requests as http_requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-isso-em-producao")

# ─── Configuração Google OAuth ────────────────────────────────────────────────
GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI  = os.environ.get("GOOGLE_REDIRECT_URI")
DONO_EMAIL           = os.environ.get("DONO_EMAIL")

GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_URL  = "https://www.googleapis.com/oauth2/v3/userinfo"

# ─── Conexão com MongoDB ──────────────────────────────────────────────────────
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client    = MongoClient(MONGO_URI)
db        = client["blog"]
colecao   = db["posts"]


# ─── Helpers de autenticação ──────────────────────────────────────────────────
def usuario_logado():
    return session.get("email") == DONO_EMAIL

def requer_login(f):
    """Decorator que protege rotas de admin."""
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


# ─── Rotas de autenticação ────────────────────────────────────────────────────
@app.route("/login")
def login():
    params = {
        "client_id":     GOOGLE_CLIENT_ID,
        "redirect_uri":  GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope":         "openid email profile",
        "prompt":        "select_account",
    }
    url = GOOGLE_AUTH_URL + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    # DEBUG — mostra a URL gerada antes de redirecionar
    return f"URL gerada: <a href='{url}'>{url}</a>"

@app.route("/login/callback")
def login_callback():
    code = request.args.get("code")
    if not code:
        return "Login cancelado.", 400

    token_resp = http_requests.post(GOOGLE_TOKEN_URL, data={
        "code":          code,
        "client_id":     GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri":  GOOGLE_REDIRECT_URI,
        "grant_type":    "authorization_code",
    })
    token_data   = token_resp.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return f"Erro ao autenticar. Resposta do Google: {token_data}", 400

    user_resp = http_requests.get(GOOGLE_USER_URL,
                                  headers={"Authorization": f"Bearer {access_token}"})
    user_info = user_resp.json()
    email     = user_info.get("email")

    # DEBUG — remove depois que funcionar
    return f"Email recebido: '{email}' | Email esperado: '{DONO_EMAIL}'"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ─── Rotas protegidas (só o dono) ────────────────────────────────────────────
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