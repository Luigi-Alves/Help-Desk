# 🚀 Guia de Configuração Inicial - Sistema de Help Desk

## 📋 Pré-requisitos

- **Python 3.7+** instalado
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para controle de versão)

## 🔧 Instalação

### Passo 1: Verificar Python
```bash
python --version
```
Você deve ver algo como: `Python 3.x.x`

### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install werkzeug
pip install flask
pip install flask-jwt-extended
```

### Passo 3: Criar Usuários de Teste
```bash
python criar_usuarios_teste.py
```

Este script criará:
- 1 Administrador
- 2 Técnicos
- 2 Usuários comuns

Todos com senha: **123**

## ▶️ Executar o Sistema

### Terminal (CLI)
```bash
python helpdesk.py
```

### API REST (Flask)
```bash
python app.py
```

Acesse em: `http://localhost:5000`

### API Simples
```bash
python api.py
```

## 📁 Estrutura do Projeto

```
Help Desk/
├── 📄 helpdesk.py              ← Sistema principal (CLI)
├── 📄 app.py                   ← API com autenticação JWT
├── 📄 api.py                   ← API simples
├── 📄 chamado.py               ← Classe Chamado
├── 📄 gera_hash.py             ← Gerador de hash
├── 📄 criar_usuarios_teste.py  ← Script de setup
│
├── 📊 usuarios.json            ← Base de dados de usuários
├── 📊 chamados.json            ← Base de dados de chamados
├── 📊 login.json               ← Exemplo de login
├── 📊 register.json            ← Exemplo de registro
│
├── 📖 README.md                ← Documentação principal
├── 📖 SETUP.md                 ← Este arquivo
├── 📖 GUIA_TESTES.md           ← Guia de testes
└── 📖 requirements.txt         ← Dependências do projeto
```

## 🎯 Primeiro Acesso

### 1. Abra o Terminal
Navigate para a pasta do projeto:
```bash
cd "c:\Users\luigi\OneDrive\Área de Trabalho\Help Desk"
```

### 2. Execute o Script de Setup
```bash
python criar_usuarios_teste.py
```

Você verá:
```
🔐 CRIADOR DE USUÁRIOS DE TESTE

✅ Usuários de teste criados com sucesso!

📋 Credenciais de teste (todos com senha '123'):
──────────────────────────────────────────
👨‍💼 ADMINISTRADOR:
  Email: admin
  Senha: 123
  Tipo: Admin - Acesso completo
...
```

### 3. Inicie o Sistema
```bash
python helpdesk.py
```

### 4. Faça Login
```
🔐 SISTEMA DE LOGIN
Email: admin
Senha: 123
```

### 5. Explore o Menu
Você verá o menu principal com todas as opções disponíveis para admin.

## 👥 Credenciais de Teste

Todos os usuários têm senha **123**:

| Email | Nome | Tipo | Permissões |
|-------|------|------|------------|
| admin | Administrador | Admin | Acesso completo |
| joao@helpdesk.com | João Silva | Técnico | Gerencia seus chamados |
| maria@helpdesk.com | Maria Santos | Técnico | Gerencia seus chamados |
| pedro@empresa.com | Pedro Oliveira | Comum | Abre/acompanha chamados |
| ana@empresa.com | Ana Costa | Comum | Abre/acompanha chamados |

## ⚙️ Configurações Importantes

### Arquivo: `usuarios.json`
Armazena todos os usuários do sistema.
- As senhas são **hashadas** (não em texto plano)
- Para adicionar usuários, use o menu dentro do aplicativo

### Arquivo: `chamados.json`
Armazena todos os chamados abertos.
- Persiste automaticamente
- Inclui rastreamento de datas e técnico responsável

## 🔐 Segurança

- ✅ Senhas **NUNCA** são armazenadas em texto plano
- ✅ Hash bcrypt (via werkzeug)
- ✅ Controle de acesso por tipo de usuário
- ✅ Dados validados antes de salvar

## 🎮 Primeiras Ações Recomendadas

### 1. Explorar como Admin
```
1. Login: admin / 123
2. Abrir um chamado (opção 1)
3. Listar chamados (opção 2)
6. Ver relatório (opção 6)
```

### 2. Cadastrar Novo Usuário
```
1. Login as admin
2. Opção 7 (Cadastrar novo usuário)
3. Preencha campos
```

### 3. Testar como Técnico
```
1. Logout (opção 9)
2. Login: joao@helpdesk.com / 123
3. Explore opções do técnico
```

### 4. Testar como Usuário Comum
```
1. Logout
2. Login: pedro@empresa.com / 123
3. Explore opções de usuário comum
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'werkzeug'"
```bash
pip install werkzeug
```

### Erro: "FileNotFoundError: usuarios.json"
Execute o script de criação de usuários:
```bash
python criar_usuarios_teste.py
```

### Erro: "UnicodeDecodeError" com caracteres especiais
Verifique que seu terminal está configurado para UTF-8.

### Sistema lento ao abrir/fechar chamados
Verifique permissões de escrita no diretório do projeto.

## 📚 Documentação

- **README.md** - Documentação completa do sistema
- **GUIA_TESTES.md** - Casos de teste detalhados
- **SETUP.md** - Este arquivo (configuração)

## ✅ Checklist de Instalação

- [ ] Python 3.7+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Usuários de teste criados (`python criar_usuarios_teste.py`)
- [ ] Sistema inicia sem erros (`python helpdesk.py`)
- [ ] Login funciona com admin/123
- [ ] Consegue abrir um chamado
- [ ] Consegue listar chamados
- [ ] Consegue fazer logout

## 🚀 Próximas Etapas

1. **Leia o README.md** para entender todas as funcionalidades
2. **Execute os testes** seguindo GUIA_TESTES.md
3. **Customize credenciais** deletando usuarios.json e criando novos
4. **Integre com banco de dados** (opcional, para produção)

## 📞 Dúvidas Comuns

**P**: Posso mudar as senhas dos usuários de teste?  
**R**: Sim, entre como admin e use a opção de cadastro para criar novo usuário.

**P**: Onde os dados são salvos?  
**R**: Em arquivos JSON na mesma pasta do projeto (usuarios.json e chamados.json).

**P**: Posso usar em produção?  
**R**: Não recomendado. Para produção, recomenda-se banco de dados SQL e HTTPS.

---

**Pronto!** 🎉 Seu sistema de Help Desk está configurado e pronto para uso!
