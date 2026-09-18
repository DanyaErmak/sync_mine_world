import os
import shutil
from pathlib import Path
from datetime import datetime
import webbrowser
from lexicon import LEXICON_RU
from find_java import find_java
from func import *

server_folder_name = 'Minecraft_server'

cloud_D = Path('D:/GoogleDrivee')
cloud_C = Path('C:/GoogleDrive')
cloud_G = Path('G:/')

cloud_dir = None
for path in [cloud_D, cloud_C, cloud_G]:
    if path.exists():
        found_folder = list(path.glob('**/Minecraft_shared'))
        if found_folder:
            cloud_dir = found_folder[0]
            break

if cloud_dir is None:
    cloud_dir = Path('G:/Мой диск/Minecraft_shared')
    cloud_dir = waiting_right_path(cloud_dir, LEXICON_RU['no_cloud_folder'])

lock_file = cloud_dir / 'world.lock'
cloud_zip = cloud_dir / f'{server_folder_name}.zip'
local_server_folder = Path.home() / 'Desktop' / server_folder_name
local_server_folder.mkdir(parents=True, exist_ok=True)

print(LEXICON_RU['sync_mine'])
choice: str = None
while choice != '0':
    choice = input(LEXICON_RU['choice']).strip()
    if choice == '1':
        if is_server_running():
            print(LEXICON_RU['server_running'])
            continue
        if not lock_file.exists():
            print(LEXICON_RU['find_java'])
            java = find_java()

            if not java:
                inp = input(LEXICON_RU['error_java']).strip(' "')
                if inp.lower() == 'i':
                    webbrowser.open(url=LEXICON_RU['link_java25'])
                    webbrowser.open(url=LEXICON_RU['link_docs_java25'])
                    print(LEXICON_RU['install_java'])
                    input(LEXICON_RU['exit'])
                    continue

                elif inp == '':
                    continue
                elif inp == '0':
                    exit()

                else:
                    path_java = Path(inp)
                    path_folder = waiting_right_path(path_java, LEXICON_RU['input_path_to_java'])
                    if (path_folder / 'java.exe').exists():
                        java = f'"{path_folder / 'java.exe'}"'
                    else:
                        print(LEXICON_RU['not_found_java.exe'])
                        continue

            print(LEXICON_RU['del_old_files_server'])
            for item in local_server_folder.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

            print(LEXICON_RU['install_folder_server'])
            shutil.unpack_archive(cloud_zip, local_server_folder)

            write_to_start_file(local_server_folder / 'start.bat', java)
            lock_server(lock_file)
            update_players_base(cloud_dir)

            print(LEXICON_RU['ready_server'])
        else:
            with open(lock_file, 'r', encoding='utf-8') as lf:
                print(f'\nМир занят компьютером: {lf.read()}\nПодключайся к нему!')
                inp = input(LEXICON_RU['exit'])
                if inp == '0':
                    exit()
                continue

    elif choice == '2':
        current_host = os.getlogin()

        if lock_file.exists():
            with open(lock_file, 'r', encoding='utf-8') as file:
                current_host = file.read().strip()

        if current_host != os.getlogin():
            print(LEXICON_RU['error_launch'])
            print(f'Имя комьютера, который сейчас является хостом: {current_host}')
            continue

        if cloud_zip.exists():
            print(LEXICON_RU['create_backup'])
            date_backup = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            path_backup = cloud_dir / f'{server_folder_name}_backup_{date_backup}.zip'

            shutil.copy2(str(cloud_zip), path_backup)
            print(LEXICON_RU['created_backup'])

        all_backups = list(cloud_dir.glob('*_backup_*.zip'))
        if len(all_backups) > 5:
            min(all_backups, key = lambda x: x.stat().st_mtime_ns).unlink()
            print(LEXICON_RU['del_backup'])

        print(LEXICON_RU['make_archive'])
        shutil.make_archive(
            base_name=str(cloud_dir / server_folder_name),
            format='zip',
            root_dir=str(local_server_folder),
        )

        if lock_file.exists():
            lock_file.unlink()
        print(LEXICON_RU['loaded_archive'])
    elif choice == '0':
        pass
    else:
        print(LEXICON_RU['bad_choice'])