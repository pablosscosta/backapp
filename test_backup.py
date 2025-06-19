import django
import os
import sys

# Configura Django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backapp.settings")
django.setup()

from backup_app.backup import run_backup

# Define a máquina e as pastas de backup (gerais)
machine_name = 'clicir-04'
backup_folders = ['Tasy']  # pode adicionar outras pastas aqui se quiser

# Executa o backup (usuários são detectados automaticamente)
run_backup(machine_name, backup_folders, user_folders=[])  # user_folders será ignorado
