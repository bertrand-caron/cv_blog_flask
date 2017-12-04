from typing import Dict, Any
from yaml import load

def get_config() -> Dict[str, Any]:
    try:
        return load(open('config/config.yml').read())
    except:
        raise Exception('ERROR: Missing config/config.yml file.')

CONFIG = get_config()
