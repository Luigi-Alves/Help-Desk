"""
Script para criar usuários de teste com senhas hashadas
Execute este script após o primeiro login para criar usuários de teste
"""

from werkzeug.security import generate_password_hash
import json

def adicionar_usuario_teste():
    usuarios = []
    
    # Carregar usuários existentes
    try:
        with open("usuarios.json", "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        pass
    
    print("\n" + "="*50)
    print("🔐 CRIADOR DE USUÁRIOS DE TESTE")
    print("="*50)
    
    # Admin (senha: 123)
    usuarios.append({
        "id": 1,
        "nome": "Administrador",
        "email": "admin",
        "senha": generate_password_hash("123"),
        "tipo": "admin"
    })
    
    # Técnico 1 (senha: 123)
    usuarios.append({
        "id": 2,
        "nome": "João Silva",
        "email": "joao@helpdesk.com",
        "senha": generate_password_hash("123"),
        "tipo": "tecnico"
    })
    
    # Técnico 2 (senha: 123)
    usuarios.append({
        "id": 3,
        "nome": "Maria Santos",
        "email": "maria@helpdesk.com",
        "senha": generate_password_hash("123"),
        "tipo": "tecnico"
    })
    
    # Usuário comum 1 (senha: 123)
    usuarios.append({
        "id": 4,
        "nome": "Pedro Oliveira",
        "email": "pedro@empresa.com",
        "senha": generate_password_hash("123"),
        "tipo": "comum"
    })
    
    # Usuário comum 2 (senha: 123)
    usuarios.append({
        "id": 5,
        "nome": "Ana Costa",
        "email": "ana@empresa.com",
        "senha": generate_password_hash("123"),
        "tipo": "comum"
    })
    
    # Salvar no arquivo
    with open("usuarios.json", "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    
    print("\n✅ Usuários de teste criados com sucesso!")
    print("\n📋 Credenciais de teste (todos com senha '123'):")
    print("-"*50)
    print("\n👨‍💼 ADMINISTRADOR:")
    print("  Email: admin")
    print("  Senha: 123")
    print("  Tipo: Admin - Acesso completo")
    
    print("\n🔧 TÉCNICOS:")
    print("  Email: joao@helpdesk.com")
    print("  Nome: João Silva")
    print("  Senha: 123")
    print()
    print("  Email: maria@helpdesk.com")
    print("  Nome: Maria Santos")
    print("  Senha: 123")
    
    print("\n👤 USUÁRIOS COMUNS:")
    print("  Email: pedro@empresa.com")
    print("  Nome: Pedro Oliveira")
    print("  Senha: 123")
    print()
    print("  Email: ana@empresa.com")
    print("  Nome: Ana Costa")
    print("  Senha: 123")
    
    print("\n" + "="*50)
    print("Agora execute: python helpdesk.py")
    print("="*50 + "\n")

if __name__ == "__main__":
    adicionar_usuario_teste()
