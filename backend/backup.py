"""
backup.py - Sistema automático de backup
Realiza backups periódicos do banco de dados com verificação de integridade
"""

import os
import shutil
import schedule
import sqlite3
import hashlib
import threading
from datetime import datetime, timedelta
from database import db, Backup

BACKUP_DIR = './backups'
DB_PATH = 'instance/helpdesk.db'  # SQLite default

def criar_diretorio_backups():
    """Cria diretório de backups se não existir"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Diretório '{BACKUP_DIR}' criado")
def calcular_hash_md5(arquivo):
    """Calcula hash MD5 de um arquivo para verificação de integridade
    
    Args:
        arquivo (str): Caminho do arquivo
    
    Returns:
        str: Hash MD5 do arquivo
    """
    hash_md5 = hashlib.md5()
    try:
        with open(arquivo, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Erro ao calcular hash: {e}")
        return None


def backup_sqlite():
    """Backup completo do banco SQLite
    
    Copia o arquivo .db e registra no banco de dados
    
    Returns:
        bool: True se bem-sucedido
    """
    criar_diretorio_backups()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_backup = f'helpdesk_backup_{timestamp}.db'
    caminho_backup = os.path.join(BACKUP_DIR, arquivo_backup)
    
    try:
        # Verificar se banco existe
        if not os.path.exists(DB_PATH):
            print(f"Banco de dados não encontrado em {DB_PATH}")
            return False
        
        # Copiar banco de dados
        shutil.copy2(DB_PATH, caminho_backup)
        
        # Calcular tamanho e hash
        tamanho = os.path.getsize(caminho_backup)
        hash_md5 = calcular_hash_md5(caminho_backup)
        
        # Registrar no banco de dados
        registro_backup = Backup(
            arquivo=arquivo_backup,
            caminho=os.path.abspath(caminho_backup),
            tamanho_bytes=tamanho,
            hash_md5=hash_md5
        )
        db.session.add(registro_backup)
        db.session.commit()
        
        tamanho_kb = tamanho / 1024
        print(f"Backup criado: {arquivo_backup} ({tamanho_kb:.2f} KB)")
        return True
        
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return False


def backup_sql_export():
    """Exporta dados para arquivo SQL (dump)
    
    Útil para portabilidade entre diferentes bancos de dados
    
    Returns:
        bool: True se bem-sucedido
    """
    criar_diretorio_backups()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_sql = f'helpdesk_export_{timestamp}.sql'
    caminho_sql = os.path.join(BACKUP_DIR, arquivo_sql)
    
    try:
        if not os.path.exists(DB_PATH):
            print(f"Banco de dados não encontrado em {DB_PATH}")
            return False
        
        conn = sqlite3.connect(DB_PATH)
        
        with open(caminho_sql, 'w', encoding='utf-8') as f:
            for linha in conn.iterdump():
                f.write(f'{linha}\n')
        
        conn.close()
        
        tamanho = os.path.getsize(caminho_sql)
        tamanho_kb = tamanho / 1024
        print(f"SQL exportado: {arquivo_sql} ({tamanho_kb:.2f} KB)")
        return True
        
    except Exception as e:
        print(f"Erro ao exportar SQL: {e}")
        return False


def limpar_backups_antigos(dias=30):
    """Remove backups com mais de X dias
    
    Args:
        dias (int): Dias de retenção
    """
    criar_diretorio_backups()
    
    limite_tempo = datetime.now() - timedelta(days=dias)
    contador = 0
    
    try:
        for arquivo in os.listdir(BACKUP_DIR):
            if not arquivo.startswith('helpdesk_backup_'):
                continue  # Ignorar outros arquivos
            
            caminho = os.path.join(BACKUP_DIR, arquivo)
            
            if os.path.isfile(caminho):
                tempo_arquivo = datetime.fromtimestamp(os.path.getmtime(caminho))
                
                if tempo_arquivo < limite_tempo:
                    try:
                        os.remove(caminho)
                        contador += 1
                        print(f"Deletado: {arquivo} (com mais de {dias} dias)")
                    except Exception as e:
                        print(f"Erro ao deletar {arquivo}: {e}")
        
        print(f"{contador} backups antigos removidos")
        
    except Exception as e:
        print(f"Erro ao limpar backups: {e}")


def restaurar_backup(arquivo_backup):
    """Restaura um backup anterior
    
    CUIDADO: Isso sobrescreverá o banco atual!
    
    Args:
        arquivo_backup (str): Nome do arquivo no diretório backups/
    
    Returns:
        bool: True se bem-sucedido
    """
    caminho_backup = os.path.join(BACKUP_DIR, arquivo_backup)
    
    if not os.path.exists(caminho_backup):
        print(f"Arquivo {arquivo_backup} não encontrado")
        return False
    
    try:
        # Criar backup do atual antes de restaurar
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_seguranca = f'pre_restore_{timestamp}.db'
        caminho_seguranca = os.path.join(BACKUP_DIR, backup_seguranca)
        
        if os.path.exists(DB_PATH):
            shutil.copy2(DB_PATH, caminho_seguranca)
            print(f"Backup de segurança criado: {backup_seguranca}")
        shutil.copy2(caminho_backup, DB_PATH)
        print(f"Backup restaurado: {arquivo_backup}")
        print("REINICIE A APLICAÇÃO para carregar o novo banco!")
        return True
        
    except Exception as e:
        print(f"Erro ao restaurar: {e}")
        return False


def verificar_integridade_backup(arquivo_backup, hash_esperado):
    """Verifica integridade de um backup comparando hashes
    
    Args:
        arquivo_backup (str): Nome do arquivo
        hash_esperado (str): Hash MD5 esperado
    
    Returns:
        bool: True se hash coincide
    """
    caminho = os.path.join(BACKUP_DIR, arquivo_backup)
    
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {arquivo_backup}")
        return False
    
    hash_calculado = calcular_hash_md5(caminho)
    
    if hash_calculado == hash_esperado:
        print(f"Integridade verificada: {arquivo_backup}")
        return True
    else:
        print(f"FALHA NA INTEGRIDADE: {arquivo_backup}")
        print(f"   Esperado: {hash_esperado}")
        print(f"   Obtido:   {hash_calculado}")
        return False


def agendar_backups():
    """Agenda backups automáticos
    
    Configurações:
    - Backup .db a cada 6 horas
    - Backup SQL diário às 02:00
    - Limpeza de backups antigos diariamente às 03:00
    """
    schedule.every(6).hours.do(backup_sqlite)
    schedule.every().day.at("02:00").do(backup_sql_export)
    schedule.every().day.at("03:00").do(lambda: limpar_backups_antigos(dias=30))
    
    print("Backups agendados:")
    print("   Backup .db a cada 6 horas")
    print("   Backup SQL diário às 02:00")
    print("   Limpeza às 03:00")


def processar_agendamentos():
    """Processa backups agendados
    
    Execute em thread separada:
    
    backup_thread = threading.Thread(target=processar_agendamentos, daemon=True)
    backup_thread.start()
    """
    while True:
        schedule.run_pending()
        import time
        time.sleep(60)  # Verificar a cada 1 minuto


def listar_backups():
    """Lista todos os backups disponíveis
    
    Returns:
        list: Lista de arquivos de backup
    """
    criar_diretorio_backups()
    
    backups = []
    for arquivo in sorted(os.listdir(BACKUP_DIR), reverse=True):
        if not arquivo.startswith('helpdesk_backup_'):
            continue
        
        caminho = os.path.join(BACKUP_DIR, arquivo)
        tamanho = os.path.getsize(caminho)
        tempo = datetime.fromtimestamp(os.path.getmtime(caminho))
        
        backups.append({
            'arquivo': arquivo,
            'tamanho_kb': round(tamanho / 1024, 2),
            'criado_em': tempo.isoformat()
        })
    
    return backups


def status_backups():
    """Retorna status dos backups
    
    Returns:
        dict: Informações sobre backups
    """
    backups = listar_backups()
    
    return {
        'total_backups': len(backups),
        'backups': backups,
        'diretorio': os.path.abspath(BACKUP_DIR),
        'estatisticas': {
            'tamanho_total_mb': sum(b['tamanho_kb'] for b in backups) / 1024,
            'backup_mais_recente': backups[0]['criado_em'] if backups else None
        }
    }
