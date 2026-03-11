# 🏢 Sistema de Gestão de Chamados (Help Desk)

Sistema completo de Help Desk desenvolvido em Python com controle de acesso baseado em perfis de usuário. Permite abertura, acompanhamento, atualização e fechamento de chamados internos com gerenciamento de técnicos e relatórios avançados.

## ✨ Funcionalidades Principais

### 🔐 Sistema de Autenticação e Controle de Acesso

- **Login seguro** com hash de senha (werkzeug)
- **Três tipos de usuários** com permissões diferentes:
  - **Administrador (Admin)**: Acesso completo ao sistema
  - **Técnico**: Gerenciamento de chamados atribuídos
  - **Usuário Comum**: Abertura e acompanhamento de próprios chamados

### 👤 Perfis de Usuário

#### 👨‍💼 Administrador
- ✅ Cadastrar novos usuários
- ✅ Abrir/listar/gerenciar chamados
- ✅ Atribuir técnicos aos chamados
- ✅ Atualizar status e fechar chamados
- ✅ Acessar relatórios completos
- ✅ Visualizar lista de todos os usuários

#### 🔧 Técnico
- ✅ Listar chamados atribuídos
- ✅ Atualizar status dos chamados
- ✅ Fechar chamados
- ✅ Abrir chamados
- ✅ Visualizar relatório de seus chamados

#### 👤 Usuário Comum
- ✅ Abrir novos chamados
- ✅ Acompanhar status dos próprios chamados
- ✅ Visualizar relatório pessoal

### 📋 Funcionalidades de Chamados

- **Abertura de chamados** com preenchimento de:
  - Nome do solicitante
  - Setor
  - Descrição do problema
  - Criação automática de ID, status e datas

- **Campos de rastreamento**:
  - ID único automático
  - Status (Aberto, Em andamento, Fechado)
  - Data de criação
  - Data de atualização
  - Data de fechamento
  - Técnico atribuído

- **Listagem inteligente**:
  - Admin: Visualiza todos os chamados
  - Técnico: Visualiza apenas chamados atribuídos a ele
  - Usuário Comum: Visualiza apenas seus próprios chamados

- **Atualização de status**:
  - Aberto → Em andamento → Fechado
  - Apenas admin e técnico podem atualizar

- **Atribuição de técnico**:
  - Apenas admin pode atribuir
  - Seleção de técnico disponível
  - Atualização automática de data

### 📊 Sistema de Relatórios

#### Relatório do Administrador
- Total de chamados no sistema
- Estatísticas por status (Aberto, Em andamento, Fechado)
- Taxa de conclusão percentual
- Distribuição por setor
- Distribuição por técnico

#### Relatório do Técnico
- Total de chamados atribuídos
- Estatísticas de seus chamados
- Taxa de conclusão pessoal

#### Relatório do Usuário Comum
- Total de chamados abertos
- Estatísticas de seus chamados
- Taxa de conclusão

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Werkzeug** - Hash seguro de senhas
- **JSON** - Persistência de dados
- **Estruturas de dados nativas** - list, dict

## 📁 Estrutura de Arquivos

```
├── helpdesk.py          # Sistema principal (CLI)
├── app.py               # API REST com Flask/JWT (alternativa)
├── api.py               # API simples (primeira versão)
├── chamado.py           # Classe Chamado (modelagem)
├── gera_hash.py         # Gerador de hash para senhas
├── usuarios.json        # Base de dados de usuários
├── chamados.json        # Base de dados de chamados
├── login.json           # Arquivo de exemplo de login
├── register.json        # Arquivo de exemplo de registro
└── README.md            # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- Bibliotecas: `werkzeug`

### Instalação de dependências
```bash
pip install werkzeug
```

### Executar o sistema
```bash
python helpdesk.py
```

## 📝 Exemplo de Uso

### 1. Login
```
🔐 SISTEMA DE LOGIN
Email: admin
Senha: 123
✅ Bem-vindo, Administrador!
   Tipo de acesso: ADMIN
```

### 2. Menu Admin
```
==================================================
🔐 SISTEMA DE CHAMADOS | Usuário: Administrador (ADMIN)
==================================================

📋 MENU ADMINISTRATIVO
1 - Abrir chamado
2 - Listar todos os chamados
3 - Atualizar status do chamado
4 - Atribuir técnico a um chamado
5 - Fechar chamado
6 - Relatório completo
7 - Cadastrar novo usuário
8 - Listar usuários
9 - Logout
0 - Sair
```

### 3. Relatório
```
============================================================
📊 RELATÓRIO COMPLETO - ADMINISTRADOR
============================================================
Total de chamados: 5
  ✓ Abertos: 2
  ⚙️ Em andamento: 2
  ✔️ Fechados: 1

Taxa de conclusão: 20.0%

--- Chamados por Setor ---
TI: 3 total | 1 abertos | 1 fechados
RH: 2 total | 1 abertos | 0 fechados

--- Chamados por Técnico ---
joao@email.com: 3 chamados
maria@email.com: 2 chamados
============================================================
```

## 🔒 Segurança

- Senhas são armazenadas com hash seguro (bcrypt equivalente)
- Senhas não são armazenadas em texto plano
- Verificação de credenciais na autenticação
- Controle de acesso por tipo de usuário em todas as operações

## 📊 Dados Persistidos

### usuarios.json
```json
{
  "id": 1,
  "nome": "Nome do Usuário",
  "email": "email@example.com",
  "senha": "hash_bcrypt_aqui",
  "tipo": "admin|tecnico|comum"
}
```

### chamados.json
```json
{
  "id": 1,
  "nome": "Solicitante",
  "setor": "TI",
  "descricao": "Descrição do problema",
  "status": "Aberto|Em andamento|Fechado",
  "criador": "email@example.com",
  "tecnico_atribuido": "tecnico@example.com ou null",
  "data_criacao": "10/03/2026 14:30:00",
  "data_atualizacao": "10/03/2026 15:00:00",
  "data_fechamento": "null ou data"
}
```

## 🎯 Fluxo de Trabalho Típico

1. **Usuário Comum** abre um novo chamado
2. **Admin** visualiza e atribui um técnico
3. **Técnico** recebe e atualiza status para "Em andamento"
4. **Técnico** fecha o chamado quando resolvido
5. **Usuário Comum** acompanha o progresso
6. **Admin** gera relatórios para análise

## 🔧 Melhorias Futuras

- [ ] Integração com banco de dados (SQLite/PostgreSQL)
- [ ] Backup automático do banco de dados SQL
- [ ] Migração automática JSON → SQL com backup inteligente
- [ ] Sistema de comentários em chamados
- [ ] Notificações por email
- [ ] Busca e filtros avançados
- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Sistema de avaliação de satisfação
- [ ] Histórico de alterações completo
- [ ] Integração com APIs externas

## 📄 Licença

Projeto educacional. Use livremente.

## 👨‍💻 Autor

Sistema de Help Desk v2.0 com controle de acesso por perfil de usuário.

---
**Última atualização**: 11 de março de 2026
