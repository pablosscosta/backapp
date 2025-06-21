from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from backup_app.backup import run_backup
from io import StringIO
import sys

def index(request):
    return render(request, 'backup_app/index.html')


def executar_backup(request):
    if request.method == 'POST':
        machine_name = request.POST.get('machine_name')
        if not machine_name:
            return render(request, 'backup_app/result.html', {'error': 'Informe o nome da máquina.'})

        print(f'Backup iniciado para a máquina: {machine_name}')
        # Aqui chama sua função run_backup passando machine_name
        # Exemplo:
        backup_folders = ['Tasy']  # ou como você estiver definindo
        user_folders = []  # se for usar

        logs = run_backup(machine_name, backup_folders, user_folders)

        return render(request, 'backup_app/result.html', {'logs': logs})

    # Se não for POST, redireciona para a página inicial
    return render(request, 'backup_app/index.html')

