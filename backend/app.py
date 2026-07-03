from pathlib import Path
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import threading
import os
from datetime import datetime

base_dir = Path(__file__).resolve().parent
instance_dir = base_dir / 'instance'
instance_dir.mkdir(parents=True, exist_ok=True)

# ===== IMPORTAÇÕES DAS NOVAS FUNCIONALIDADES =====
from database import db, Usuario, Chamado, LogAuditoria, Backup
from auditoria import registrar_auditoria, obter_historico_chamado, relatorio_auditoria
from backup import agendar_backups, processar_agendamentos, backup_sqlite, listar_backups
from migrate import executar_migracao

# ===== CONFIGURAÇÃO DO FLASK =====
app = Flask(__name__)
@app.route('/')
def index():
    return jsonify({
        "sistema": "Helpdesk API",
        "status": "online",
        "endpoints_disponiveis": ["/login", "/register", "/chamados"]
    }), 200

# Configurações do banco de dados
database_path = instance_dir / 'helpdesk.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path.as_posix()}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'sua-chave-secreta-muito-segura')

# Inicializar extensões
db.init_app(app)
jwt = JWTManager(app)

# ===== INICIALIZAÇÃO DO BANCO E BACKUPS =====
with app.app_context():
    # Criar todas as tabelas
    db.create_all()
    print("Banco de dados pronto!")
    
    # APENAS NA PRIMEIRA VEZ: descomente para migrar de JSON
    # executar_migracao(app)

# Agendar backups automáticos
agendar_backups()
backup_thread = threading.Thread(target=processar_agendamentos, daemon=True)
backup_thread.start()
print("Sistema de backups iniciado!")

# ===== AUTENTICAÇÃO (atualizada com auditoria) =====

@app.post('/register')
def register():
    """Registrar novo usuário"""
    data = request.json
    
    # Validações
    if not all(k in data for k in ['nome', 'email', 'senha', 'tipo']):
        return jsonify({"msg": "Campos obrigatórios: nome, email, senha, tipo"}), 400
    
    if not data['tipo'] in ['admin', 'tecnico', 'usuario']:
        return jsonify({"msg": "Tipo inválido"}), 400
    
    # Verificar se usuário já existe
    if Usuario.query.filter_by(email=data['email']).first():
        registrar_auditoria(0, 'registro_falha', 'usuarios', 
                          dados_novos={'email': data['email'], 'motivo': 'já existe'})
        return jsonify({"msg": "Usuário já existe!"}), 400
    
    # Criar novo usuário
    novo_usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=generate_password_hash(data['senha']),
        tipo=data['tipo']
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    # Registrar na auditoria
    registrar_auditoria(novo_usuario.id, 'criar', 'usuarios',
                       dados_novos={'id': novo_usuario.id, 'email': novo_usuario.email, 'tipo': novo_usuario.tipo})
    
    return jsonify({"msg": "Usuário registrado com sucesso!", "id": novo_usuario.id}), 201


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Fazer login com auditoria"""

    if request.method == 'GET':
        return jsonify({"msg": "Endpoint de login ativo. Para entrar, envie uma requisição POST com suas credenciais."}), 200


    data = request.json
    
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if not usuario or not check_password_hash(usuario.senha, data['senha']):
        # Registrar tentativa falhada
        registrar_auditoria(0, 'login_falha', 'usuarios', 
                          dados_novos={'email': data['email']})
        return jsonify({"msg": "Credenciais inválidas!"}), 401
    
    # Criar token
    # Flask-JWT-Extended espera identity como string (subject)
    subject = f"{usuario.id}:{usuario.email}:{usuario.tipo}"
    access_token = create_access_token(identity=subject)


    
    # Registrar login bem-sucedido
    registrar_auditoria(usuario.id, 'login', 'usuarios', 
                       dados_novos={'email': usuario.email})
    
    return jsonify({
        "access_token": access_token,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "tipo": usuario.tipo
        }
    }), 200


# ===== CHAMADOS (com auditoria) =====

@app.post('/chamados')
@jwt_required()
def abrir_chamado():
    """Abrir novo chamado"""
    identity_raw = get_jwt_identity()
    try:
        id_str, email_str, tipo_str = identity_raw.split(':', 2)
        identidade = {
            'id': int(id_str),
            'email': email_str,
            'tipo': tipo_str
        }
    except Exception:
        return jsonify({"msg": "Identidade inválida no token"}), 401
    data = request.json

    
    if not all(k in data for k in ['nome', 'setor', 'descricao']):
        return jsonify({"msg": "Campos obrigatórios: nome, setor, descricao"}), 400
    
    novo_chamado = Chamado(
        usuario_id=identidade['id'],
        nome_solicitante=data['nome'],
        setor=data['setor'],
        descricao=data['descricao']
    )
    
    db.session.add(novo_chamado)
    db.session.commit()
    
    # Registrar na auditoria
    registrar_auditoria(identidade['id'], 'criar', 'chamados',
                       dados_novos={
                           'id': novo_chamado.id,
                           'nome': novo_chamado.nome_solicitante,
                           'setor': novo_chamado.setor
                       },
                       chamado_id=novo_chamado.id)
    
    return jsonify({
        "msg": "Chamado aberto com sucesso!",
        "id": novo_chamado.id,
        "status": novo_chamado.status
    }), 201


@app.get('/chamados/<int:chamado_id>')
@jwt_required()
def obter_chamado(chamado_id):
    """Obter detalhes de um chamado"""
    chamado = Chamado.query.get(chamado_id)
    
    if not chamado:
        return jsonify({"msg": "Chamado não encontrado"}), 404
    
    return jsonify(chamado.to_dict()), 200


@app.put('/chamados/<int:chamado_id>')
@jwt_required()
def atualizar_chamado(chamado_id):
    """Atualizar status de um chamado"""
    identidade = get_jwt_identity()
    chamado = Chamado.query.get(chamado_id)
    
    if not chamado:
        return jsonify({"msg": "Chamado não encontrado"}), 404
    
    data = request.json
    dados_anteriores = {'status': chamado.status}
    
    # Verificar permissões (simplificado)
    if identidade['tipo'] not in ['admin', 'tecnico']:
        return jsonify({"msg": "Acesso negado"}), 403
    
    if 'status' in data:
        chamado.status = data['status']
        if data['status'] == 'Fechado':
            chamado.fechado_em = datetime.utcnow()
    
    db.session.commit()
    
    # Registrar mudança na auditoria
    registrar_auditoria(identidade['id'], 'atualizar', 'chamados',
                       dados_anteriores=dados_anteriores,
                       dados_novos={'status': chamado.status},
                       chamado_id=chamado_id)
    
    return jsonify({
        "msg": "Chamado atualizado",
        "chamado": chamado.to_dict()
    }), 200


# ===== ENDPOINTS DE AUDITORIA (ADMIN ONLY) =====

@app.get('/admin/auditoria/chamado/<int:chamado_id>')
@jwt_required()
def auditoria_chamado(chamado_id):
    """Histórico completo de um chamado"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    logs = obter_historico_chamado(chamado_id)
    return jsonify({
        "chamado_id": chamado_id,
        "total_eventos": len(logs),
        "eventos": logs
    }), 200


@app.get('/admin/auditoria/usuario/<int:usuario_id>')
@jwt_required()
def auditoria_usuario(usuario_id):
    """Histórico de ações de um usuário"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    from auditoria import obter_historico_usuario
    logs = obter_historico_usuario(usuario_id)
    
    return jsonify({
        "usuario_id": usuario_id,
        "total_ações": len(logs),
        "ações": logs
    }), 200


@app.get('/admin/auditoria/relatorio')
@jwt_required()
def relatorio_auditoria_endpoint():
    """Relatório geral de auditoria com filtros"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    # Parâmetros de filtro
    dias = request.args.get('dias', 7, type=int)
    acao = request.args.get('acao', None)
    
    from datetime import timedelta
    data_inicio = datetime.utcnow() - timedelta(days=dias)
    
    logs = relatorio_auditoria(data_inicio=data_inicio, acao=acao)
    
    return jsonify({
        "periodo_dias": dias,
        "data_inicio": data_inicio.isoformat(),
        "total_registros": len(logs),
        "registros": logs
    }), 200


@app.get('/admin/auditoria/compliance')
@jwt_required()
def compliance_report():
    """Relatório de compliance consolidado"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    from auditoria import gerar_relatorio_compliance
    relatorio = gerar_relatorio_compliance(periodo_dias=30)
    
    return jsonify(relatorio), 200


# ===== ENDPOINTS DE BACKUP (ADMIN ONLY) =====

@app.post('/admin/backup/agora')
@jwt_required()
def fazer_backup_agora():
    """Fazer backup manual imediatamente"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    if backup_sqlite():
        registrar_auditoria(identidade['id'], 'backup', 'sistema')
        return jsonify({"msg": "Backup realizado com sucesso!"}), 200
    else:
        return jsonify({"msg": "Erro ao criar backup"}), 500


@app.get('/admin/backups')
@jwt_required()
def listar_backups_endpoint():
    """Listar todos os backups disponíveis"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    backups = Backup.query.order_by(Backup.criado_em.desc()).all()
    
    return jsonify({
        "total": len(backups),
        "backups": [b.to_dict() for b in backups]
    }), 200


@app.post('/admin/backup/restaurar/<int:backup_id>')
@jwt_required()
def restaurar_backup_endpoint(backup_id):
    """Restaurar um backup específico"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    backup = Backup.query.get(backup_id)
    if not backup:
        return jsonify({"msg": "Backup não encontrado"}), 404
    
    from backup import restaurar_backup
    if restaurar_backup(backup.arquivo):
        registrar_auditoria(identidade['id'], 'restaurar_backup', 'sistema',
                          dados_novos={'backup_id': backup_id})
        return jsonify({
            "msg": "Backup restaurado! REINICIE A APLICAÇÃO",
            "backup": backup.arquivo
        }), 200
    else:
        return jsonify({"msg": "Erro ao restaurar backup"}), 500


@app.get('/admin/backup/status')
@jwt_required()
def status_backup():
    """Status do sistema de backups"""
    identidade = get_jwt_identity()
    
    if identidade['tipo'] != 'admin':
        return jsonify({"msg": "Apenas admins"}), 403
    
    from backup import status_backups
    return jsonify(status_backups()), 200


# ===== ERRO HANDLERS =====

@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify({"msg": "Rota não encontrada"}), 404


@app.errorhandler(500)
def erro_interno(e):
    return jsonify({"msg": "Erro interno do servidor"}), 500


# ===== MAIN =====

if __name__ == '__main__':
    print("=" * 50)
    print(" Servidor Help Desk iniciando...")
    print("=" * 50)
    print()
    print(" Banco de dados: SQLite")
    print(" Autenticação: JWT")
    print(" Auditoria: Ativada")
    print(" Backups: Agendados")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
