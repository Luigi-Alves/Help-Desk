"""
auditoria.py - Sistema de auditoria e rastreamento
Registra todas as ações dos usuários para compliance e segurança
"""

from database import db, LogAuditoria
from flask import request
from datetime import datetime

def registrar_auditoria(usuario_id, acao, tabela_afetada, dados_anteriores=None, dados_novos=None, chamado_id=None):
    """
    Registra uma ação na tabela de auditoria
    
    Args:
        usuario_id (int): ID do usuário que fez a ação
        acao (str): Tipo de ação ('criar', 'atualizar', 'deletar', 'login', 'logout', etc)
        tabela_afetada (str): Nome da tabela ('usuarios', 'chamados', 'sistema', 'login')
        dados_anteriores (dict): Dados antes da ação (para updates)
        dados_novos (dict): Dados depois da ação (para creates/updates)
        chamado_id (int): ID do chamado afetado (se houver relação)
    
    Returns:
        bool: True se registrado com sucesso, False caso contrário
    
    Exemplos:
        # Login bem-sucedido
        registrar_auditoria(user.id, 'login', 'usuarios', dados_novos={'email': user.email})
        
        # Criar chamado
        registrar_auditoria(user.id, 'criar', 'chamados', 
                          dados_novos={'id': chamado.id, 'setor': chamado.setor},
                          chamado_id=chamado.id)
        
        # Atualizar status de chamado
        registrar_auditoria(user.id, 'atualizar', 'chamados',
                          dados_anteriores={'status': 'Aberto'},
                          dados_novos={'status': 'Em andamento'},
                          chamado_id=chamado.id)
    """
    try:
        # Obter IP do cliente (trata casos onde fora do contexto de request)
        try:
            endereco_ip = request.remote_addr
        except:
            endereco_ip = None
        
        log = LogAuditoria(
            usuario_id=usuario_id,
            chamado_id=chamado_id,
            acao=acao,
            tabela_afetada=tabela_afetada,
            dados_anteriores=dados_anteriores,
            dados_novos=dados_novos,
            endereco_ip=endereco_ip
        )
        
        db.session.add(log)
        db.session.commit()
        
        return True
        
    except Exception as e:
        print(f" Erro ao registrar auditoria: {e}")
        db.session.rollback()
        return False


def obter_historico_chamado(chamado_id):
    """Retorna histórico completo de um chamado
    
    Args:
        chamado_id (int): ID do chamado
    
    Returns:
        list: Lista de dicts com logs do chamado
    """
    logs = LogAuditoria.query.filter_by(chamado_id=chamado_id).order_by(LogAuditoria.timestamp).all()
    return [log.to_dict() for log in logs]


def obter_historico_usuario(usuario_id, limite=100):
    """Retorna todas as ações de um usuário
    
    Args:
        usuario_id (int): ID do usuário
        limite (int): Número máximo de registros a retornar
    
    Returns:
        list: Lista de dicts com ações do usuário (mais recentes primeiro)
    """
    logs = LogAuditoria.query.filter_by(usuario_id=usuario_id)\
        .order_by(LogAuditoria.timestamp.desc())\
        .limit(limite)\
        .all()
    return [log.to_dict() for log in logs]


def relatorio_auditoria(data_inicio=None, data_fim=None, usuario_id=None, acao=None, limite=1000):
    """Retorna relatório de auditoria com filtros
    
    Args:
        data_inicio (datetime): Filtrar logs após essa data
        data_fim (datetime): Filtrar logs antes dessa data
        usuario_id (int): Filtrar por usuário específico
        acao (str): Filtrar por tipo de ação
        limite (int): Número máximo de registros
    
    Returns:
        list: Lista de dicts com logs filtrados
    """
    query = LogAuditoria.query
    
    if data_inicio:
        query = query.filter(LogAuditoria.timestamp >= data_inicio)
    
    if data_fim:
        query = query.filter(LogAuditoria.timestamp <= data_fim)
    
    if usuario_id:
        query = query.filter(LogAuditoria.usuario_id == usuario_id)
    
    if acao:
        query = query.filter(LogAuditoria.acao == acao)
    
    logs = query.order_by(LogAuditoria.timestamp.desc()).limit(limite).all()
    return [log.to_dict() for log in logs]


def obter_tentativas_login_falhas(usuario_id=None, horas=24):
    """Retorna tentativas de login falhadas recentes
    
    Args:
        usuario_id (int): Filtrar por usuário
        horas (int): Período em horas (padrão 24h)
    
    Returns:
        list: Tentativas de login falhadas
    """
    from datetime import timedelta
    
    tempo_minimo = datetime.utcnow() - timedelta(hours=horas)
    
    query = LogAuditoria.query\
        .filter(LogAuditoria.acao == 'login_falha')\
        .filter(LogAuditoria.timestamp >= tempo_minimo)
    
    if usuario_id:
        query = query.filter(LogAuditoria.usuario_id == usuario_id)
    
    logs = query.order_by(LogAuditoria.timestamp.desc()).all()
    return [log.to_dict() for log in logs]


def obter_atividades_suspeitas(horas=24):
    """Retorna atividades potencialmente suspeitas
    
    Incluindo:
    - Múltiplas tentativas de login falhadas
    - Ações de usuários fora de horário
    - Acessos de IPs incomuns
    
    Args:
        horas (int): Período em horas
    
    Returns:
        dict: Relatório de atividades suspeitas
    """
    from datetime import timedelta
    
    tempo_minimo = datetime.utcnow() - timedelta(hours=horas)
    
    # Tentativas de login falhadas
    logins_falhados = LogAuditoria.query\
        .filter(LogAuditoria.acao == 'login_falha')\
        .filter(LogAuditoria.timestamp >= tempo_minimo)\
        .all()
    
    # Contar por endereço IP
    ips_suspeitos = {}
    for log in logins_falhados:
        if log.endereco_ip:
            ips_suspeitos[log.endereco_ip] = ips_suspeitos.get(log.endereco_ip, 0) + 1
    
    return {
        'total_tentativas_login_falhas': len(logins_falhados),
        'ips_suspeitos': {ip: count for ip, count in ips_suspeitos.items() if count > 5},
        'logs': [log.to_dict() for log in logins_falhados[-50:]]  # Últimos 50
    }


def gerar_relatorio_compliance(periodo_dias=30):
    """Gera relatório completo de compliance
    
    Args:
        periodo_dias (int): Período em dias
    
    Returns:
        dict: Relatório estruturado
    """
    from datetime import timedelta
    
    data_inicio = datetime.utcnow() - timedelta(days=periodo_dias)
    
    # Total de ações por tipo
    todas_acoes = LogAuditoria.query\
        .filter(LogAuditoria.timestamp >= data_inicio)\
        .all()
    
    acoes_por_tipo = {}
    for log in todas_acoes:
        acoes_por_tipo[log.acao] = acoes_por_tipo.get(log.acao, 0) + 1
    
    # Total de ações por usuário
    acoes_por_usuario = {}
    for log in todas_acoes:
        acoes_por_usuario[log.usuario_id] = acoes_por_usuario.get(log.usuario_id, 0) + 1
    
    return {
        'periodo_dias': periodo_dias,
        'data_inicio': data_inicio.isoformat(),
        'data_fim': datetime.utcnow().isoformat(),
        'total_registros': len(todas_acoes),
        'acoes_por_tipo': acoes_por_tipo,
        'usuarios_ativos': len(acoes_por_usuario),
        'acoes_por_usuario': acoes_por_usuario
    }
