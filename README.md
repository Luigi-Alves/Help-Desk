# 🏢 HelpDesk API – Sistema de Gestão de Chamados

API REST desenvolvida em Python para gerenciamento de chamados técnicos internos, com autenticação baseada em JWT e controle de acesso por perfil de usuário.

Este projeto simula um ambiente corporativo real, aplicando conceitos fundamentais de backend, segurança e organização modular.

---

## 🚀 Visão Geral

O sistema permite que usuários autenticados abram e acompanhem chamados, enquanto técnicos e administradores possuem permissões ampliadas para gerenciamento.

O projeto evoluiu de uma aplicação CLI simples para uma API estruturada, refletindo uma progressão prática no aprendizado de arquitetura backend.

---

## 🔐 Principais Funcionalidades

### 👤 Autenticação e Usuários
- Registro de novos usuários
- Login com geração de token JWT
- Senhas armazenadas com hash seguro
- Controle de acesso por perfil:
  - Admin
  - Técnico
  - Usuário comum

### 📋 Gestão de Chamados
- Abertura de chamados
- Listagem de chamados
- Atualização de status
- Fechamento de chamados
- Restrições de acesso baseadas em perfil

---

## 🛠️ Stack Tecnológica

- Python 3
- Flask
- Flask-JWT-Extended
- Werkzeug (hash de senha)
- Persistência em JSON
- Estrutura modular organizada por responsabilidade

---

## 🧱 Arquitetura

O projeto segue separação clara de responsabilidades:

- `auth` → autenticação e controle de acesso  
- `chamados` → regras de negócio  
- `models` → estrutura de dados  
- `app.py` → inicialização da aplicação  

A autenticação é feita via token JWT, garantindo proteção de rotas e controle por nível de usuário.

---

## ⚙️ Como Executar

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/helpdesk-api.git

# Entrar na pasta
cd helpdesk-api

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
