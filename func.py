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
