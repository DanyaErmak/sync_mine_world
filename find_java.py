import subprocess
from pathlib import Path
from lexicon import LEXICON_RU
from functools import wraps

def _check_java() -> bool:
    '''Проверяет наличие нужной версии джавы в системе'''
    good_versions = ['21.', '22.', '23.', '24.', '25.', '26.']
    try:
        result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if any(i for i in good_versions if f'java version "{i}"' in result.stderr):
            return True
        return False
    except FileNotFoundError:
        print(LEXICON_RU['no_java'])
    return False

def _check_java_in_launchers(path: Path = None, *,tlauncher: bool = True) -> Path | bool:
    '''Ищет в лаунчере самую высокую версию джавы и возвращает путь до неё'''
    if path is None:
        path = Path.home() / 'AppData/Roaming/.minecraft/runtime'

    folders_java = list(path.glob('java-runtime-*'))
    if not folders_java:
        return False
    new_java = max(folders_java)

    folder_windows = 'windows' if tlauncher else 'windows-x64'
    return new_java / folder_windows / new_java.stem / 'bin' / 'java.exe'

def find_java() -> str | bool:
    '''Общая функция для поиска джавы'''
    tlauncher_java = _check_java_in_launchers()
    legacy_java = _check_java_in_launchers(tlauncher=False)
    chosen_java = False

    if tlauncher_java and tlauncher_java.exists():
        chosen_java = f'"{tlauncher_java}"'
        print('Обнаружена Java от TLauncher')
    elif legacy_java and legacy_java.exists():
        chosen_java = f'"{legacy_java}"'
        print('Обнаружена Java от Legacy Launcher')
    elif _check_java():
        chosen_java = 'java'
        print('Обнаружена java в системе')

    return chosen_java