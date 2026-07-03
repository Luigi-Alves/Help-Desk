"""
Configurações do projeto Help Desk
"""

import os
from pathlib import Path

# Caminho do banco SQLite
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "helpdesk.db"
BACKUP_DIR = BASE_DIR / "backups"

# Criar diretório de backups se não existir
BACKUP_DIR.mkdir(exist_ok=True)

# URL do banco para SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH.absolute()}"

# Config backup
BACKUP_FILE_PREFIX = "helpdesk_backup"

