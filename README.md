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
python main.py
