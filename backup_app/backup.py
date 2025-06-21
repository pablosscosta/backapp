import os
import shutil
from pathlib import Path
from datetime import datetime

def get_users_modified_in_2025(users_root: Path) -> list:
    """
    Retorna uma lista com os nomes de usuários cujas pastas em C:\\Users
    foram modificadas no ano de 2025, ignorando junções e pastas do sistema.
    """
    filtered_users = []
    IGNORED_USERNAMES = {
        'all users', 'default', 'default user', 'public',
        'desktop.ini', 'usuário padrão', 'user', 'users', 'defaultuser0'
    }

    if not users_root.exists():
        return filtered_users

    for user_dir in users_root.iterdir():
        try:
            if (
                user_dir.is_dir()
                and not user_dir.is_symlink()
                and user_dir.name.lower() not in IGNORED_USERNAMES
            ):
                last_modified = datetime.fromtimestamp(user_dir.stat().st_mtime)
                if last_modified.year == 2025:
                    filtered_users.append(user_dir.name)
        except Exception as e:
            print(f"[AVISO] Erro ao verificar pasta {user_dir.name}: {e}")

    return filtered_users


def copy_folder(src: Path, dest: Path):
    """
    Copia uma pasta inteira de src para dest,
    ignorando erros como arquivos não encontrados, problemas de permissão,
    e links simbólicos específicos como "Meus Vídeos", "Minhas Imagens", etc.
    """
    ignore_names = {'Meus Vídeos', 'Minhas Imagens', 'Minhas Músicas'}

    def ignore_func(folder, contents):
        return [item for item in contents if item in ignore_names]

    try:
        shutil.copytree(
            src,
            dest,
            dirs_exist_ok=True,
            ignore=ignore_func,
            ignore_dangling_symlinks=True
        )
        print(f'Backup da pasta "{src.name}" concluído.')
    except shutil.Error as e:
        for src_path, dest_path, error_msg in e.args[0]:
            if 'Acesso negado' in error_msg:
                # Ignora erro de acesso negado
                continue
            print(f"[AVISO] {src_path} => {error_msg}")
    except FileNotFoundError as e:
        print(f"[AVISO] Arquivo não encontrado durante a cópia: {e}")
    except Exception as e:
        print(f"[ERRO] Falha ao copiar {src} => {e}")


def copy_appdata_filtered(src_appdata: Path, dest_appdata: Path, logs: list):
    """
    Copia somente as pastas específicas dentro de AppData, ignorando erros de arquivos em uso e acesso negado.
    """
    if not src_appdata.exists():
        logs.append(f"Pasta AppData não existe em {src_appdata}")
        return

    folders_to_copy = ['Google', 'Mozilla', 'Thunderbird']

    for folder_name in folders_to_copy:
        src_folder = src_appdata / folder_name
        if src_folder.exists():
            dest_folder = dest_appdata / folder_name
            try:
                shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True, ignore_dangling_symlinks=True)
                logs.append(f'Backup da pasta "{src_folder}" concluído.')
            except shutil.Error as e:
                logs.append(f"[AVISO] Alguns arquivos não puderam ser copiados de {src_folder}:")
                for src_path, dest_path, error_msg in e.args[0]:
                    # Ignora arquivos em uso e acesso negado
                    if '[WinError 32]' in error_msg or 'Acesso negado' in error_msg:
                        continue
                    logs.append(f" - {src_path} => {error_msg}")
            except Exception as e:
                logs.append(f"[ERRO] Falha ao copiar {src_folder}: {e}")
        else:
            logs.append(f"Pasta {src_folder} não existe, pulando.")


def copy_user_folders(user_path: Path, dest_root: Path, logs: list):
    folders_to_copy = ["Desktop", "Documents", "Downloads", "Videos", "Pictures", "Music"]

    for folder_name in folders_to_copy:
        src_folder = user_path / folder_name
        dest_folder = dest_root / folder_name

        if src_folder.exists() and src_folder.is_dir():
            try:
                shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True, ignore_dangling_symlinks=True)
                logs.append(f'Backup da pasta "{folder_name}" concluído para o usuário {user_path.name}.')
            except shutil.Error as e:
                logs.append(f"[AVISO] Alguns arquivos não puderam ser copiados de {src_folder}:")
                for src_path, dest_path, error_msg in e.args[0]:
                    # Ignora arquivos em uso e acesso negado
                    if '[WinError 32]' in error_msg or 'Acesso negado' in error_msg:
                        continue
                    logs.append(f" - {src_path} => {error_msg}")
            except Exception as e:
                logs.append(f"[ERRO] Falha ao copiar {src_folder}: {e}")
        else:
            logs.append(f'Pasta "{folder_name}" não encontrada para o usuário {user_path.name}, pulando.')


def run_backup(machine_name, backup_folders, user_folders):
    logs = []

    dest_root = Path(f'D:/backup/{machine_name}')
    dest_root.mkdir(parents=True, exist_ok=True)

    # Backup de pastas gerais
    for folder_path in backup_folders:
        src = Path(f'\\\\{machine_name}\\C$') / folder_path
        dest = dest_root / folder_path.replace('\\', '_')

        if src.exists():
            try:
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
                logs.append(f'Backup da pasta "{folder_path}" concluído.')
            except Exception as e:
                logs.append(f'[ERRO] Falha ao copiar pasta "{folder_path}": {e}')
        else:
            logs.append(f'Pasta "{folder_path}" não encontrada na máquina "{machine_name}".')

    # Backup dos usuários modificados em 2025
    users_root = Path(f"\\\\{machine_name}\\C$\\Users")
    user_folders = get_users_modified_in_2025(users_root)

    funcionarios_ti = ['pablo.silva']
    USUARIOS_IGNORADOS = {'administrador', 'default', 'defaultuser0', 'public', 'user'}
    USUARIOS_IGNORADOS.update(user.lower() for user in funcionarios_ti)

    for user in user_folders:
        if user.lower() in USUARIOS_IGNORADOS:
            logs.append(f'Usuário "{user}" ignorado no backup.')
            continue
        src_user = users_root / user
        dest_user = dest_root / 'Users' / user

        if not src_user.exists():
            logs.append(f'Usuário "{user}" não encontrado na máquina "{machine_name}".')
            continue

        copy_user_folders(src_user, dest_user, logs)

        src_appdata_local = src_user / 'AppData' / 'Local'
        dest_appdata_local = dest_user / 'AppData' / 'Local'
        if src_appdata_local.exists():
            copy_appdata_filtered(src_appdata_local, dest_appdata_local, logs)

        src_appdata_roaming = src_user / 'AppData' / 'Roaming'
        dest_appdata_roaming = dest_user / 'AppData' / 'Roaming'
        if src_appdata_roaming.exists():
            copy_appdata_filtered(src_appdata_roaming, dest_appdata_roaming, logs)

        logs.append(f'Backup do usuário "{user}" concluído.')

    return logs
