"""
migrate.py - Migração de dados JSON para SQL
Execute uma única vez para migrar dados existentes
"""

import json
from datetime import datetime
from database import db, Usuario, Chamado

def migrar_usuarios_json():
    """Migra usuários do JSON (usuarios.json) para SQL"""
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
        
        if not isinstance(usuarios, list):
            print("Formato inválido em usuarios.json")
            return 0
        
        migrados = 0
        for user in usuarios:
            # Verificar se já existe
            existe = Usuario.query.filter_by(email=user['email']).first()
            if existe:
                print(f"Usuário {user['email']} já existe - pulando")
                continue
            
            novo_usuario = Usuario(
                nome=user['nome'],
                email=user['email'],
                senha=user['senha'],  # Já em hash
                tipo=user.get('tipo', 'usuario')
            )
            db.session.add(novo_usuario)
            migrados += 1
        
        db.session.commit()
        print(f"✅ {migrados} usuários migrados com sucesso!")
        return migrados
        
    except FileNotFoundError:
        print("Arquivo usuarios.json não encontrado")
        return 0
    except Exception as e:
        print(f"Erro na migração de usuários: {e}")
        db.session.rollback()
        return 0


def migrar_chamados_json():
    
    try:
        with open('chamados.json', 'r', encoding='utf-8') as f:
            chamados = json.load(f)
        
        if not isinstance(chamados, list):
            print("Formato inválido em chamados.json")
            return 0
        
        migrados = 0
        for chamado_dados in chamados:
            # Tentar encontrar o usuário criador do chamado
            usuario_email = chamado_dados.get('usuario') or chamado_dados.get('email') or chamado_dados.get('criador')
            
            if not usuario_email:
                print(f"Chamado {chamado_dados.get('id')} não tem usuário criador - pulando")
                continue
            
            usuario = Usuario.query.filter_by(email=usuario_email).first()
            if not usuario:
                print(f"Usuário {usuario_email} não encontrado para chamado {chamado_dados.get('id')}")
                continue
            
            tecnico_id = None
            tecnico_email = chamado_dados.get('tecnico_atribuido')
            if tecnico_email:
                tecnico = Usuario.query.filter_by(email=tecnico_email).first()
                if tecnico:
                    tecnico_id = tecnico.id
            
            data_criacao = chamado_dados.get('data_criacao')
            criado_em = datetime.now()
            if data_criacao:
                try:
                    criado_em = datetime.strptime(data_criacao, '%d/%m/%Y %H:%M:%S')
                except ValueError:
                    criado_em = datetime.now()
            
            novo_chamado = Chamado(
                usuario_id=usuario.id,
                nome_solicitante=chamado_dados.get('nome', 'N/A'),
                setor=chamado_dados.get('setor', 'N/A'),
                descricao=chamado_dados.get('descricao', ''),
                status=chamado_dados.get('status', 'Aberto'),
                tecnico_id=tecnico_id,
                criado_em=criado_em
            )
            db.session.add(novo_chamado)
            migrados += 1
        
        db.session.commit()
        print(f"{migrados} chamados migrados com sucesso!")
        return migrados
        
    except FileNotFoundError:
        print("Arquivo chamados.json não encontrado")
        return 0
    except Exception as e:
        print(f"Erro na migração de chamados: {e}")
        db.session.rollback()
        return 0


def executar_migracao(app):
    """Executa todas as migrações do JSON para SQL
    
    Use assim no seu app.py:
    
    from migrate import executar_migracao
    
    if __name__ == '__main__':
        # Executar UMA ÚNICA VEZ
        executar_migracao(app)
        # Depois comente/remova esta linha
        
        app.run(debug=True)
    """
    with app.app_context():
        print("=" * 50)
        print("INICIANDO MIGRAÇÃO JSON -> SQL")
        print("=" * 50)
        print()
        
        # Criar todas as tabelas
        print("Criando tabelas do banco de dados...")
        db.create_all()
        print("Tabelas criadas com sucesso\n")
        
        # Migrar dados
        print("Migrando usuários...")
        usuarios_migrados = migrar_usuarios_json()
        print()
        
        print("Migrando chamados...")
        chamados_migrados = migrar_chamados_json()
        print()
        
        # Resumo
        print("=" * 50)
        print(f"MIGRAÇÃO CONCLUÍDA!")
        print(f"   Total de usuários: {usuarios_migrados}")
        print(f"   Total de chamados: {chamados_migrados}")
        print("=" * 50)


if __name__ == '__main__':
    # Para testar isoladamente
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    executar_migracao(app)
