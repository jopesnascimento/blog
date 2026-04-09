# 📰 Blog Pessoal com Flask

Aplicação web dinâmica desenvolvida com Python e Flask para criação e gerenciamento de posts, com autenticação de usuário e persistência em MongoDB.

## 🌐 Acesse a aplicação

👉 https://SEU-LINK-DO-RENDER-AQUI

_(Projeto em produção — deploy realizado com Render)_

---

## 🚀 Sobre o projeto

Este projeto começou como um blog simples com persistência em JSON e evoluiu para uma aplicação mais robusta, incorporando autenticação e banco de dados NoSQL.

O objetivo foi simular um sistema real de publicação de conteúdo, aplicando conceitos fundamentais de desenvolvimento web, backend e estruturação de aplicações.

---

## 🧠 Funcionalidades

- 🔐 Sistema de login para acesso administrativo
- 📝 CRUD completo de posts (criar, editar, deletar)
- 📄 Visualização individual de posts
- 🗂️ Persistência de dados com MongoDB
- 📅 Data de publicação automática
- ✅ Validação de formulários
- 🎨 Interface responsiva com Tailwind CSS

---

## 🛠️ Tecnologias utilizadas

**Backend**

- Python 3.x
- Flask
- PyMongo

**Frontend**

- HTML5
- Jinja2 Templates
- Tailwind CSS

**Infraestrutura**

- Render (deploy)

**Banco de dados**

- MongoDB

---

## 📁 Estrutura do projeto

blog-flask/
│
├── app/
│ ├── routes.py
│ ├── auth.py
│ ├── models.py
│ ├── templates/
│ └── static/
│
├── config.py
├── run.py
├── requirements.txt
└── README.md

---

## ⚙️ Como rodar localmente

### 1. Clone o repositório

git clone https://github.com/jopesnascimento/portifolio-jornalistico.git  
cd portifolio-jornalistico

### 2. Ambiente virtual

python -m venv .venv

# Windows

.venv\Scripts\activate

# Linux/Mac

source .venv/bin/activate

### 3. Dependências

pip install -r requirements.txt

### 4. Configuração

MONGO_URI = "mongodb://localhost:27017/blog_db"

### 5. Executar

python run.py

---

## 🔐 Autenticação

O sistema possui autenticação básica para proteger rotas administrativas.

_(Sugestão futura: implementar hash de senha e controle de sessão mais robusto)_

---

## 📈 Próximas melhorias

- [ ] Hash de senha (bcrypt)
- [ ] Cadastro de usuários
- [ ] Busca de posts
- [ ] Categorias e tags
- [ ] Paginação
- [ ] Melhorar UX do painel admin

---

## 💡 Aprendizados

- Evolução de JSON para MongoDB
- Estruturação de aplicação Flask
- Implementação de autenticação
- Construção de CRUD completo
- Deploy de aplicação em produção

---

## 👨‍💻 Autor

João Pedro Souza do Nascimento  
https://github.com/jopesnascimento

---

## 📄 Licença

MIT
