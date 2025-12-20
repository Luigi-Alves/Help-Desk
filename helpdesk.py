def menu():
    print("\n=== SISTEMA DE CHAMADOS ===")
    print("1 - Abrir chamado")
    print("2 - Listar chamados")
    print("3 - Atualizar status do chamado")
    print("4 - Fechar chamado")
    print("5 - Relatório")
    print("6 - Sair")


def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Abrir chamado (em desenvolvimento)")
        elif opcao == "2":
            print("Listar chamados (em desenvolvimento)")
        elif opcao == "3":
            print("Atualizar status (em desenvolvimento)")
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
