from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

#Funções auxiliares
def carregar_post():
    try:
        with open('post.json',"r",encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    
def salvar_post():
    with open('post.json','w',encoding="utf-8") as arquivo:
        json.dump(posts,arquivo, indent=2, ensure_ascii=False)

posts = carregar_post()


#app - sempre coloco isso para não me perder
@app.route("/")
def home_page():
    return render_template("index.html",posts=posts)

@app.route("/post/<int:post_id>")
def post_detalhes(post_id):

    for post in posts:
        if post["id"] == post_id:
            return render_template("post.html",post=post)
        
    return "Post não encontrado",404
@app.route("/novo")
def novo_post():
    return render_template("novo.html")

@app.route("/criar", methods = ["POST"])
def criar_post():
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    autor = request.form['autor']

    if len(posts) == 0:
        novo_id = 1
    else:
        novo_id = posts[-1]["id"] + 1

    novo_post = {
        "id": novo_id,
        "titulo":titulo,
        "conteudo":conteudo,
        "autor":autor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    if not titulo.strip():
        return "Título não pode estar vazio", 400
    
    if not conteudo.strip():
        return "Conteúdo não pode estar vazio", 400
    
    if not autor.strip():
        return "Autor não pode estar vazio", 400

    posts.append(novo_post)
    salvar_post()
    return redirect('/')


@app.route('/editar/<int:post_id>')
def editar_post(post_id):
    
    for post in posts:
        if post["id"] == post_id:
       
            return render_template("editar.html", post=post)
  
    return "Post não encontrado", 404
@app.route("/atualizar/<int:post_id>", methods=["POST"])
def atualizar_post(post_id):
    # Procurar o post pelo ID
    for post in posts:
        if post['id'] == post_id:
            post["titulo"] = request.form["titulo"]
            post["conteudo"] = request.form["conteudo"]
            post["autor"] = request.form["autor"]
            salvar_post()
            return redirect(f"/post/{post_id}")
        
    return "Post não encontrado",404
@app.route("/deletar/<int:post_id>",methods=['POST'])
def deletar_post(post_id):
    for post in posts:
 
        if post["id"] == post_id:
            posts.remove(post)
            salvar_post()
            return redirect("/")
    return('Post não encontrado',404)
