from typing import Dict, Any
from yaml import safe_load
from os.path import dirname, abspath, join

def get_config() -> Dict[str, Any]:
    path: str = join(dirname(dirname(abspath(__file__))), 'config/config.yml')
    try:
        return safe_load(open(path).read())
    except Exception as e:
        print(e)
        raise Exception(f'ERROR: Missing {path} file.') from e

CONFIG = get_config()
