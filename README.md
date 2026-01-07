# 📝 Blog Pessoal com Flask

Blog dinâmico e responsivo construído com Flask, Jinja2 e Tailwind CSS, com persistência em JSON.

## 🚀 Funcionalidades

- ✅ Criar, editar e deletar posts
- ✅ Visualização individual de posts
- ✅ Persistência de dados em JSON
- ✅ Design responsivo com Tailwind CSS
- ✅ Validação de formulários
- ✅ Data de publicação automática
- ✅ Interface limpa e moderna

## 🛠️ Tecnologias

- **Backend:** Python 3.x, Flask
- **Frontend:** HTML5, Jinja2 Templates, Tailwind CSS
- **Persistência:** JSON

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/blog-flask.git
cd blog-flask
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o servidor

```bash
flask run
```

A aplicação estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
blog-flask/
├── app.py              # Aplicação principal
├── templates/          # Templates HTML
│   ├── base.html       # Layout base
│   ├── index.html      # Página inicial
│   ├── post.html       # Página do post
│   ├── novo.html       # Criar post
│   └── editar.html     # Editar post
├── posts.json          # Banco de dados (gerado automaticamente)
├── requirements.txt    # Dependências
└── README.md          # Documentação
```

## 📚 Rotas da Aplicação

| Rota              | Método | Descrição                     |
| ----------------- | ------ | ----------------------------- |
| `/`               | GET    | Lista todos os posts          |
| `/post/<id>`      | GET    | Visualiza post específico     |
| `/novo`           | GET    | Exibe formulário de novo post |
| `/criar`          | POST   | Cria novo post                |
| `/editar/<id>`    | GET    | Exibe formulário de edição    |
| `/atualizar/<id>` | POST   | Atualiza post existente       |
| `/deletar/<id>`   | POST   | Deleta post                   |

## 🎯 Próximos Passos

- [ ] Implementar dark mode
- [ ] Adicionar sistema de categorias
- [ ] Adicionar busca de posts
- [ ] Migrar para banco de dados SQL
- [ ] Adicionar autenticação de usuários
- [ ] Implementar paginação

## 👨‍💻 Autor

João Pedro - [GitHub](https://github.com/seu-usuario)

## 📄 Licença

Este projeto está sob a licença MIT.
