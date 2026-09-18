import os
import subprocess
from pathlib import Path

def waiting_right_path(path: Path, input_text: str) -> Path:
    '''В цикле while ожидает существующий путь'''
    while not path.exists():
        user_input = input(input_text).strip(' "')

        if user_input == '0':
            exit()

        path = Path(user_input)

    return path

def lock_server(path_lock_file: Path) -> None:
    '''Записывает в lock-файл имя компьютера'''
    with open(path_lock_file, 'w', encoding='utf-8') as lf:
        lf.write(os.getlogin())

def write_to_start_file(path_start: Path, path_java: str) -> None:
    '''Записывает в файл start.bat правильный путь до джавы'''
    with open(path_start, 'w', encoding='utf-8') as file:
        file.write(f'{path_java} -Xmx4G -jar fabric-server.jar nogui\npause')

def is_server_running() -> bool:
    '''Проверяет запущен ли в данный момент сервер (то есть java.exe) на компьютере'''
    try:
        result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if 'java.exe' in result.stdout:
            return True
        return False
    except Exception:
        return False

def get_radmin_ip() -> str:
    '''Возвращает ip-адрес сетевого адаптера Radmin VPN при его наличии'''
    try:
        result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')
        for block in result.stdout.split('Адаптер'):
            if 'Radmin VPN' in block:
                for line in block.split('\n'):
                    if 'IPv4' in line:
                        ip = line.split(':')[-1].strip()
                        return ip
        return '127.0.0.1'
    except Exception:
        return '127.0.0.1'

def update_players_base(cloud_dir: Path) -> None:
    '''Обновляет или добавляет имя ПК и ip-адрес хоста '''
    ip_file = cloud_dir / 'players.txt'
    my_name = os.getlogin()
    my_ip = get_radmin_ip()

    if my_ip == "127.0.0.1":
        return

    lines = []
    player_found = False
    if ip_file.exists():
        with open(ip_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    name, ip = line.strip().spilt(':')
                    if name == my_name:
                        lines.append(f"{my_name}:{my_ip}\n")
                        player_found = True
                    else:
                        lines.append(line)

    if not player_found:
        lines.append(f'{my_name}:{my_ip}\n')

    with open(ip_file, 'w', encoding='utf-8') as file:
        file.writelines(lines)