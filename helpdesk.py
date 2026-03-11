from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

# --- Variáveis Globais ---
chamados = []
usuarios = []
usuario_logado = None
proximo_id = 1

# --- Funções de Menu ---
def menu_principal():
    tipo_usuario = usuario_logado["tipo"]
    
    print("\n" + "="*50)
    print(f"🔐 SISTEMA DE CHAMADOS | Usuário: {usuario_logado['nome']} ({tipo_usuario.upper()})")
    print("="*50)
    
    if tipo_usuario == "admin":
        print("\n📋 MENU ADMINISTRATIVO")
        print("1 - Abrir chamado")
        print("2 - Listar todos os chamados")
        print("3 - Atualizar status do chamado")
        print("4 - Atribuir técnico a um chamado")
        print("5 - Fechar chamado")
        print("6 - Relatório completo")
        print("7 - Cadastrar novo usuário")
        print("8 - Listar usuários")
        print("9 - Logout")
        print("0 - Sair")
    elif tipo_usuario == "tecnico":
        print("\n🔧 MENU TÉCNICO")
        print("1 - Listar chamados atribuídos")
        print("2 - Atualizar status do chamado")
        print("3 - Fechar chamado")
        print("4 - Abrir novo chamado")
        print("5 - Relatório de meus chamados")
        print("6 - Logout")
        print("0 - Sair")
    else:  # usuario comum
        print("\n👤 MENU DO USUÁRIO")
        print("1 - Abrir novo chamado")
        print("2 - Acompanhar meus chamados")
        print("3 - Relatório de meus chamados")
        print("4 - Logout")
        print("0 - Sair")
    
    print("="*50)

# --- Funções de Usuário ---
def cadastro_usuario():
    """Apenas administrador pode cadastrar novos usuários"""
    if usuario_logado["tipo"] != "admin":
        print("❌ Apenas administradores podem cadastrar novos usuários.")
        return
    
    global usuarios

    print("\n--- 👤 Cadastro de Novo Usuário ---")
    nome = input("Nome: ").strip()
    if not nome:
        print("❌ Nome não pode estar vazio!")
        return
    
    email = input("Email: ").strip()
    if not email:
        print("❌ Email não pode estar vazio!")
        return
    
    # Validar email existente
    if any(u["email"] == email for u in usuarios):
        print("❌ Email já cadastrado no sistema!")
        return
    
    senha = input("Senha: ").strip()
    if not senha:
        print("❌ Senha não pode estar vazia!")
        return
    
    print("\nTipos de usuário disponíveis:")
    print("1. admin - Acesso completo ao sistema")
    print("2. tecnico - Pode atualizar e fechar chamados")
    print("3. comum - Pode abrir e acompanhar seus chamados")
    
    tipo = input("Escolha o tipo (1/2/3): ").strip()
    tipo_map = {"1": "admin", "2": "tecnico", "3": "comum"}
    
    if tipo not in tipo_map:
        print("❌ Opção inválida!")
        return
    
    tipo = tipo_map[tipo]
    
    novo_usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "email": email,
        "senha": generate_password_hash(senha),
        "tipo": tipo
    }

    usuarios.append(novo_usuario)
    salvar_usuarios()
    print(f"✅ Usuário '{nome}' ({tipo}) cadastrado com sucesso!")

def listar_usuarios():
    """Lista todos os usuários (apenas admin)"""
    if usuario_logado["tipo"] != "admin":
        print("❌ Apenas administradores podem listar usuários.")
        return
    
    if not usuarios:
        print("\n📭 Nenhum usuário cadastrado.")
        return
    
    print("\n" + "="*70)
    print("👥 LISTA DE USUÁRIOS")
    print("="*70)
    print(f"{'ID':<5} {'Nome':<20} {'Email':<25} {'Tipo':<10}")
    print("-"*70)
    
    for usuario in usuarios:
        print(f"{usuario['id']:<5} {usuario['nome']:<20} {usuario['email']:<25} {usuario['tipo']:<10}")
    print("="*70)

def login():
    """Sistema de login com validação"""
    global usuario_logado

    print("\n" + "="*50)
    print("🔐 SISTEMA DE LOGIN")
    print("="*50)
    
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()

    for usuario in usuarios:
        if usuario["email"] == email and check_password_hash(usuario["senha"], senha):
            usuario_logado = usuario
            print(f"\n✅ Bem-vindo, {usuario['nome']}!")
            print(f"   Tipo de acesso: {usuario['tipo'].upper()}")
            input("Pressione ENTER para continuar...")
            return True

    print("\n❌ Credenciais inválidas! Email ou senha incorretos.")
    return False

def logout():
    """Função de logout"""
    global usuario_logado
    print(f"\n👋 Logout realizado. Até logo, {usuario_logado['nome']}!")
    usuario_logado = None

# --- Funções de Chamados ---
def abrir_chamado():
    global proximo_id

    print("\n--- 📝 Abrir Novo Chamado ---")
    nome = input("Nome do solicitante (ou ENTER para usar seu nome): ").strip()
    if not nome:
        nome = usuario_logado["nome"]
    
    setor = input("Setor: ").strip()
    if not setor:
        print("❌ Setor não pode estar vazio!")
        return
    
    descricao = input("Descrição do problema: ").strip()
    if not descricao:
        print("❌ Descrição não pode estar vazia!")
        return

    chamado = {
        "id": proximo_id,
        "nome": nome,
        "setor": setor,
        "descricao": descricao,
        "status": "Aberto",
        "criador": usuario_logado["email"],
        "tecnico_atribuido": None,
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "data_fechamento": None
    }

    chamados.append(chamado)
    proximo_id += 1
    salvar_chamados()
    print(f"\n✅ Chamado #{proximo_id - 1} aberto com sucesso!")

def listar_chamados_filtrados(filtro_tipo=None):
    """Lista chamados com filtros baseado no tipo de usuário"""
    if not chamados:
        print("\n📭 Nenhum chamado registrado.")
        return

    lista_filtrada = chamados
    
    if filtro_tipo == "meus":  # Apenas chamados criados pelo usuário
        lista_filtrada = [c for c in chamados if c["criador"] == usuario_logado["email"]]
    elif filtro_tipo == "atribuidos":  # Apenas chamados atribuídos ao técnico
        lista_filtrada = [c for c in chamados if c["tecnico_atribuido"] == usuario_logado["email"]]

    if not lista_filtrada:
        print("\n📭 Nenhum chamado encontrado.")
        return

    print("\n" + "="*100)
    print("LISTA DE CHAMADOS")
    print("="*100)
    print(f"{'ID':<5} {'Solicitante':<15} {'Setor':<12} {'Status':<15} {'Técnico':<15} {'Data Criação':<16}")
    print("-"*100)
    
    for chamado in lista_filtrada:
        tecnico = chamado["tecnico_atribuido"] if chamado["tecnico_atribuido"] else "Não atribuído"
        print(
            f"{chamado['id']:<5} {chamado['nome']:<15} {chamado['setor']:<12} "
            f"{chamado['status']:<15} {tecnico:<15} {chamado['data_criacao']:<16}"
        )
    print("="*100)

def atualizar_status():
    """Aqui somente admin e técnico podem atualizar"""
    if not chamados:
        print("\n📭 Não há chamados para atualizar.")
        return
    
    # Mostrar chamados disponíveis
    if usuario_logado["tipo"] == "tecnico":
        chamados_disponiveis = [c for c in chamados if c["tecnico_atribuido"] == usuario_logado["email"] and c["status"] != "Fechado"]
    else:
        chamados_disponiveis = [c for c in chamados if c["status"] != "Fechado"]
    
    if not chamados_disponiveis:
        print("\n📭 Nenhum chamado disponível para atualizar.")
        return
    
    print("\n--- Chamados disponíveis ---")
    for c in chamados_disponiveis:
        print(f"ID: {c['id']} | {c['nome']} | Status: {c['status']}")
    
    try:
        id_chamado = int(input("\nDigite o ID do chamado: "))
    except ValueError:
        print("❌ ID inválido. Digite um número.")
        return
    
    for chamado in chamados:
        if chamado["id"] == id_chamado:
            print(f"\n📌 Status atual: {chamado['status']}")
            print("1 - Em andamento")
            print("2 - Fechado")

            opcao = input("Escolha o novo status: ").strip()

            if opcao == "1":
                chamado["status"] = "Em andamento"
                chamado["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                salvar_chamados()
                print("✅ Status atualizado para 'Em andamento'!")
            elif opcao == "2":
                chamado["status"] = "Fechado"
                chamado["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                chamado["data_fechamento"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                salvar_chamados()
                print("✅ Chamado foi fechado com sucesso!")
            else:
                print("❌ Opção inválida!")
            return
    print("❌ Chamado não encontrado.")

def atribuir_tecnico():
    """Apenas administrador pode atribuir técnico"""
    if usuario_logado["tipo"] != "admin":
        print("❌ Apenas administradores podem atribuir técnicos.")
        return
    
    # Listar técnicos disponíveis
    tecnicos = [u for u in usuarios if u["tipo"] == "tecnico"]
    if not tecnicos:
        print("❌ Nenhum técnico cadastrado no sistema.")
        return
    
    print("\n--- Técnicos disponíveis ---")
    for i, tec in enumerate(tecnicos, 1):
        print(f"{i}. {tec['nome']} ({tec['email']})")
    
    try:
        idx_tecnico = int(input("\nEscolha o número do técnico: ")) - 1
        if idx_tecnico < 0 or idx_tecnico >= len(tecnicos):
            print("❌ Opção inválida!")
            return
        tecnico_selecionado = tecnicos[idx_tecnico]
    except ValueError:
        print("❌ Número inválido!")
        return
    
    # Listar chamados para atribuir
    chamados_abertos = [c for c in chamados if c["status"] in ["Aberto", "Em andamento"]]
    if not chamados_abertos:
        print("❌ Nenhum chamado disponível para atribuir.")
        return
    
    print("\n--- Chamados disponíveis ---")
    for c in chamados_abertos:
        print(f"ID: {c['id']} | {c['nome']} | Status: {c['status']}")
    
    try:
        id_chamado = int(input("\nDigite o ID do chamado a ser atribuído: "))
    except ValueError:
        print("❌ ID inválido!")
        return
    
    for chamado in chamados:
        if chamado["id"] == id_chamado:
            chamado["tecnico_atribuido"] = tecnico_selecionado["email"]
            chamado["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            salvar_chamados()
            print(f"✅ Chamado atribuído a {tecnico_selecionado['nome']}!")
            return
    
    print("❌ Chamado não encontrado.")

def fechar_chamado():
    """Admin e técnico podem fechar chamados"""
    if not chamados:
        print("\n📭 Não há chamados para fechar.")
        return
    
    # Listar chamados abertos
    chamados_abertos = [c for c in chamados if c["status"] != "Fechado"]
    if not chamados_abertos:
        print("\n✅ Todos os chamados já estão fechados!")
        return
    
    print("\n--- Chamados abertos ---")
    for c in chamados_abertos:
        print(f"ID: {c['id']} | {c['nome']} | Status: {c['status']}")
    
    try:
        id_chamado = int(input("\nDigite o ID do chamado a ser fechado: "))
    except ValueError:
        print("❌ ID inválido!")
        return
    
    for chamado in chamados:
        if chamado["id"] == id_chamado:
            if chamado["status"] == "Fechado":
                print("⚠️ O chamado já está fechado.")
            else:
                chamado["status"] = "Fechado"
                chamado["data_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                chamado["data_fechamento"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                salvar_chamados()
                print("✅ Chamado fechado com sucesso!")
            return
    print("❌ Chamado não encontrado.")

def relatorio():
    """Gera relatório baseado no tipo de usuário"""
    tipo = usuario_logado["tipo"]
    
    if tipo == "admin":
        relatorio_admin()
    elif tipo == "tecnico":
        relatorio_tecnico()
    else:
        relatorio_usuario_comum()

def relatorio_admin():
    """Relatório completo para administrador"""
    if not chamados:
        print("\n📭 Nenhum chamado registrado.")
        return
    
    total_chamados = len(chamados)
    abertos = sum(1 for c in chamados if c["status"] == "Aberto")
    andamento = sum(1 for c in chamados if c["status"] == "Em andamento")
    fechados = sum(1 for c in chamados if c["status"] == "Fechado")
    
    print("\n" + "="*60)
    print("📊 RELATÓRIO COMPLETO - ADMINISTRADOR")
    print("="*60)
    print(f"Total de chamados: {total_chamados}")
    print(f"  ✓ Abertos: {abertos}")
    print(f"  ⚙️ Em andamento: {andamento}")
    print(f"  ✔️ Fechados: {fechados}")
    print(f"\nTaxa de conclusão: {(fechados/total_chamados*100):.1f}%")
    
    # Por setor
    setores = {}
    for chamado in chamados:
        setor = chamado["setor"]
        if setor not in setores:
            setores[setor] = {"total": 0, "abertos": 0, "fechados": 0}
        setores[setor]["total"] += 1
        if chamado["status"] == "Aberto":
            setores[setor]["abertos"] += 1
        elif chamado["status"] == "Fechado":
            setores[setor]["fechados"] += 1
    
    print("\n--- Chamados por Setor ---")
    for setor, dados in setores.items():
        print(f"{setor}: {dados['total']} total | {dados['abertos']} abertos | {dados['fechados']} fechados")
    
    # Por técnico
    tecnicos = {}
    for chamado in chamados:
        if chamado["tecnico_atribuido"]:
            tec = chamado["tecnico_atribuido"]
            if tec not in tecnicos:
                tecnicos[tec] = 0
            tecnicos[tec] += 1
    
    if tecnicos:
        print("\n--- Chamados por Técnico ---")
        for tec, qtd in tecnicos.items():
            print(f"{tec}: {qtd} chamados")
    
    print("="*60)

def relatorio_tecnico():
    """Relatório para técnico com seus chamados"""
    chamados_tecnico = [c for c in chamados if c["tecnico_atribuido"] == usuario_logado["email"]]
    
    if not chamados_tecnico:
        print("\n📭 Você não possui chamados atribuídos.")
        return
    
    total = len(chamados_tecnico)
    abertos = sum(1 for c in chamados_tecnico if c["status"] == "Aberto")
    andamento = sum(1 for c in chamados_tecnico if c["status"] == "Em andamento")
    fechados = sum(1 for c in chamados_tecnico if c["status"] == "Fechado")
    
    print("\n" + "="*60)
    print(f"📊 RELATÓRIO DE CHAMADOS - {usuario_logado['nome'].upper()}")
    print("="*60)
    print(f"Total de chamados: {total}")
    print(f"  ✓ Abertos: {abertos}")
    print(f"  ⚙️ Em andamento: {andamento}")
    print(f"  ✔️ Fechados: {fechados}")
    print(f"\nTaxa de conclusão: {(fechados/total*100):.1f}%")
    print("="*60)

def relatorio_usuario_comum():
    """Relatório para usuário comum com seus chamados"""
    chamados_usuario = [c for c in chamados if c["criador"] == usuario_logado["email"]]
    
    if not chamados_usuario:
        print("\n📭 Você não possui chamados abertos.")
        return
    
    total = len(chamados_usuario)
    abertos = sum(1 for c in chamados_usuario if c["status"] == "Aberto")
    andamento = sum(1 for c in chamados_usuario if c["status"] == "Em andamento")
    fechados = sum(1 for c in chamados_usuario if c["status"] == "Fechado")
    
    print("\n" + "="*60)
    print(f"📊 RELATÓRIO DE MEUS CHAMADOS - {usuario_logado['nome'].upper()}")
    print("="*60)
    print(f"Total de chamados: {total}")
    print(f"  ✓ Abertos: {abertos}")
    print(f"  ⚙️ Em andamento: {andamento}")
    print(f"  ✔️ Fechados: {fechados}")
    print(f"\nTaxa de conclusão: {(fechados/total*100):.1f}%")
    print("="*60)

# --- Funções de Persistência de Dados ---
def salvar_chamados():
    with open("chamados.json", "w", encoding="utf-8") as arquivo:
        json.dump(chamados, arquivo, indent=4, ensure_ascii=False)

def carregar_chamados():
    global chamados, proximo_id
    try:
        with open("chamados.json", "r", encoding="utf-8") as arquivo:
            chamados = json.load(arquivo)
            if chamados:
                proximo_id = max(chamado["id"] for chamado in chamados) + 1
            else:
                proximo_id = 1
    except FileNotFoundError:
        chamados = []

def salvar_usuarios():
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

def carregar_usuarios():
    global usuarios
    try:
        with open("usuarios.json", "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        usuarios = []

# --- Função Principal ---
def main():
    carregar_chamados()
    carregar_usuarios()

    print("\n" + "="*50)
    print("🎯 BEM-VINDO AO SISTEMA DE HELP DESK")
    print("="*50)

    if not login():
        print("\n⚠️ Sistema encerrado.")
        return

    while usuario_logado:
        menu_principal()
        opcao = input("\nEscolha uma opção: ").strip()

        tipo = usuario_logado["tipo"]

        # --- MENU DO ADMIN ---
        if tipo == "admin":
            if opcao == "1":
                abrir_chamado()
            elif opcao == "2":
                listar_chamados_filtrados()
            elif opcao == "3":
                atualizar_status()
            elif opcao == "4":
                atribuir_tecnico()
            elif opcao == "5":
                fechar_chamado()
            elif opcao == "6":
                relatorio()
            elif opcao == "7":
                cadastro_usuario()
            elif opcao == "8":
                listar_usuarios()
            elif opcao == "9":
                logout()
            elif opcao == "0":
                print("\n👋 Encerrando o sistema...")
                break
            else:
                print("❌ Opção inválida!")

        # --- MENU DO TÉCNICO ---
        elif tipo == "tecnico":
            if opcao == "1":
                listar_chamados_filtrados("atribuidos")
            elif opcao == "2":
                atualizar_status()
            elif opcao == "3":
                fechar_chamado()
            elif opcao == "4":
                abrir_chamado()
            elif opcao == "5":
                relatorio()
            elif opcao == "6":
                logout()
            elif opcao == "0":
                print("\n👋 Encerrando o sistema...")
                break
            else:
                print("❌ Opção inválida!")

        # --- MENU DO USUÁRIO COMUM ---
        else:  # usuario_logado["tipo"] == "comum"
            if opcao == "1":
                abrir_chamado()
            elif opcao == "2":
                listar_chamados_filtrados("meus")
            elif opcao == "3":
                relatorio()
            elif opcao == "4":
                logout()
            elif opcao == "0":
                print("\n👋 Encerrando o sistema...")
                break
            else:
                print("❌ Opção inválida!")


if __name__ == "__main__":
    main()