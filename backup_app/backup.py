import os
import shutil
from pathlib import Path
from datetime import datetime

def get_users_modified_in_2025(users_root: Path) -> list:
    """
    Retorna uma lista com os nomes de usuários cujas pastas em C:\\Users
    foram modificadas no ano de 2025, ignorando junções e perfis padrão/sistema.
    """
    filtered_users = []

    # Nomes de usuários a ignorar (perfils padrão ou irrelevantes)
    excluded_names = {
        'All Users', 'Default', 'Default User', 'Public', 'desktop.ini',
        'Administrador', 'Usuário Padrão', 'user', 'Guest'
    }

    if not users_root.exists():
        return filtered_users

    for user_dir in users_root.iterdir():
        try:
            if (
                user_dir.is_dir()
                and not user_dir.is_symlink()
                and user_dir.name not in excluded_names
            ):
                last_modified = datetime.fromtimestamp(user_dir.stat().st_mtime)
                if last_modified.year == 2025:
                    filtered_users.append(user_dir.name)
        except Exception as e:
            print(f"Erro ao verificar pasta de {user_dir.name}: {e}")
    
    return filtered_users



def copy_folder(src: Path, dest: Path):
    """
    Copia uma pasta inteira de src para dest,
    ignorando erros como arquivos não encontrados e problemas de permissão.
    """
    try:
        shutil.copytree(src, dest, dirs_exist_ok=True, ignore_dangling_symlinks=True)
        print(f'Backup da pasta "{src.name}" concluído.')
    except shutil.Error as e:
        print(f"[AVISO] Alguns arquivos/pastas não puderam ser copiados de {src}:")
        for src_path, dest_path, error_msg in e.args[0]:
            print(f" - {src_path} => {error_msg}")
    except FileNotFoundError as e:
        print(f"[AVISO] Arquivo não encontrado durante a cópia: {e}")
    except Exception as e:
        print(f"[ERRO] Falha ao copiar {src} => {e}")


def copy_appdata_filtered(src_appdata: Path, dest_appdata: Path):
    """
    Copia somente as pastas específicas dentro de AppData, ignorando erros de arquivos em uso.
    """
    if not src_appdata.exists():
        print(f"Pasta AppData não existe em {src_appdata}")
        return

    folders_to_copy = ['Google', 'Mozilla', 'Thunderbird']

    for folder_name in folders_to_copy:
        src_folder = src_appdata / folder_name
        if src_folder.exists():
            dest_folder = dest_appdata / folder_name
            try:
                shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True, ignore_dangling_symlinks=True)
                print(f'Backup da pasta "{src_folder}" concluído.')
            except shutil.Error as e:
                print(f"[AVISO] Alguns arquivos não puderam ser copiados de {src_folder}:")
                for src_path, dest_path, error_msg in e.args[0]:
                    if '[WinError 32]' in error_msg:
                        print(f" - Arquivo em uso ignorado: {src_path}")
                    else:
                        print(f" - {src_path} => {error_msg}")
            except Exception as e:
                print(f"[ERRO] Falha ao copiar {src_folder}: {e}")
        else:
            print(f"Pasta {src_folder} não existe, pulando.")


def copy_user_folders(user_path: Path, dest_root: Path):
    """
    Copia as pastas específicas do nível raiz do perfil do usuário para o backup,
    evitando problemas com links simbólicos em subpastas de Documents.
    """
    folders_to_copy = [
        "Desktop",
        "Documents",
        "Downloads",
        "Videos",
        "Pictures",
        "Music"
    ]

    for folder_name in folders_to_copy:
        src_folder = user_path / folder_name
        dest_folder = dest_root / folder_name

        if src_folder.exists() and src_folder.is_dir():
            try:
                shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True, ignore_dangling_symlinks=True)
                print(f'Backup da pasta "{folder_name}" concluído para o usuário {user_path.name}.')
            except shutil.Error as e:
                print(f"[AVISO] Alguns arquivos não puderam ser copiados de {src_folder}:")
                for src_path, dest_path, error_msg in e.args[0]:
                    print(f" - {src_path} => {error_msg}")
            except Exception as e:
                print(f"[ERRO] Falha ao copiar {src_folder}: {e}")
        else:
            print(f'Pasta "{folder_name}" não encontrada para o usuário {user_path.name}, pulando.')


def run_backup(machine_name, backup_folders, user_folders):
    """
    Executa o backup das pastas especificadas da máquina.

    Parâmetros:
    - machine_name (str): Nome da máquina na rede (ex: SUP-UTIS-02)
    - backup_folders (list of str): Lista das pastas no disco C que serão copiadas para o backup
    - user_folders (list of str): Lista dos nomes das pastas de usuários que terão backup parcial (área de trabalho, documentos, etc.)

    O backup será armazenado em D:/backup/<machine_name>/

    A função copia:
    - As pastas gerais indicadas em backup_folders (cópia completa)
    - Para cada usuário modificado em 2025, copia as pastas principais (chamando copy_user_folders)
    - Copia parcialmente a pasta AppData filtrando as subpastas Google, Mozilla e Thunderbird dentro de Local e Roaming
    """

    dest_root = Path(f'D:/backup/{machine_name}')
    if not dest_root.exists():
        dest_root.mkdir(parents=True)

    # Backup das pastas gerais
    for folder_path in backup_folders:
        src = Path(f'\\\\{machine_name}\\C$') / folder_path
        dest = dest_root / folder_path.replace('\\', '_')

        if src.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            print(f'Backup da pasta "{folder_path}" concluído.')
        else:
            print(f'Pasta "{folder_path}" não encontrada na máquina "{machine_name}".')

    # Backup parcial das pastas dos usuários
    users_root = Path(f"\\\\{machine_name}\\C$\\Users")
    user_folders = get_users_modified_in_2025(users_root)

    for user in user_folders:
        src_user = users_root / user
        dest_user = dest_root / 'Users' / user

        if not src_user.exists():
            print(f'Usuário "{user}" não encontrado na máquina "{machine_name}".')
            continue

        copy_user_folders(src_user, dest_user)

        # Pasta AppData parcial
        src_appdata_local = src_user / 'AppData' / 'Local'
        dest_appdata_local = dest_user / 'AppData' / 'Local'
        if src_appdata_local.exists():
            copy_appdata_filtered(src_appdata_local, dest_appdata_local)

        src_appdata_roaming = src_user / 'AppData' / 'Roaming'
        dest_appdata_roaming = dest_user / 'AppData' / 'Roaming'
        if src_appdata_roaming.exists():
            copy_appdata_filtered(src_appdata_roaming, dest_appdata_roaming)

        print(f'Backup do usuário "{user}" concluído.')
