# Lista que armazena todos os chamados
chamados = []

#Variáveis globais para controle de IDs
proximo_id = 1

def menu():
    print("\n=== SISTEMA DE CHAMADOS ===")
    print("1 - Abrir chamado")
    print("2 - Listar chamados")
    print("3 - Atualizar status do chamado")
    print("4 - Fechar chamado")
    print("5 - Relatório")
    print("6 - Sair")

def abrir_chamado():
    global proximo_id

    print("\n--- Abrir Chamado ---")
    nome = input("Nome do solicitante: ")
    setor = input("Setor: ")
    descricao = input("Descrição do problema: ")

    chamado = {
        "id": proximo_id,
        "nome": nome,
        "setor": setor,
        "descricao": descricao,
        "status": "Aberto"
    }

    chamados.append(chamado)
    proximo_id += 1
    print("Chamado aberto com sucesso!")


def listar_chamados():
    if not chamados:
        print("Nenhum chamado registrado.")
        return

    print("\n--- Lista de Chamados ---")
    for chamado in chamados:
            print(
                f"ID: {chamado['id']} |"
                f" Nome: {chamado['nome']}|" 
                f"Setor: {chamado['setor']} |"
                f"Status: {chamado['status']}"
            )

def atualizar_status():
    if not chamados:
        print("\nNão há chamados para atualizar.")
        return
    

    try:
        id_chamado = int(input("Digite o ID do chamado:"))
    except ValueError:
        print("ID inválido. Digite um número.")
        return
    
    for chamado in chamados:
        if chamado["id"] == id_chamado:
            print("\nStatus atual:", chamado["status"])
            print("1 - Em andamento")
            print("2 - Fechado")

            opcao = input("Escolha o novo status: ")

            if opcao == "1":
                chamado["status"] = "Em andamento"
                print("Status atualizado com sucesso!")
            elif opcao == "2":
                chamado["status"] = "Fechado"
                print("Chamado fechado com sucesso!")
            else:
                print("Opção inválida!")
            return
    print("Chamado não encontrado.")

    

def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            abrir_chamado()
        elif opcao == "2":
            listar_chamados()
        elif opcao == "3":
            atualizar_status()
        elif opcao == "4":
            print("Fechar chamado (em desenvolvimento)")
        elif opcao == "5":
            print("Relatório (em desenvolvimento)")
        elif opcao == "6":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
