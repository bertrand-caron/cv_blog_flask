from typing import Dict, Any
from yaml import load

def get_config() -> Dict[str, Any]:
    try:
        return load(open('config/config.yml').read())
    except Exception as e:
        raise Exception('ERROR: Missing config/config.yml file.') from e

CONFIG = get_config()
