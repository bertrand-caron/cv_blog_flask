from sqlite3 import connect, OperationalError
from typing import Any

DB_CONN = connect('cv.db', isolation_level=None)
CURSOR = DB_CONN.cursor()

def create_tables() -> None:
    CURSOR.execute('CREATE TABLE IF NOT EXISTS logs (datetime DATETIME, ip VARCHAR(39))')

def log_access(request: Any) -> None:
    try:
        CURSOR.execute('INSERT INTO logs (datetime, ip) VALUES (DATETIME("now"), ?)', (request.environ['HTTP_X_REAL_IP'],))
    except Exception:
        pass

if __name__ == '__main__':
    try:
        from geoip import geolite2
        def get_geo(ip_address: str) -> Any:
            return geolite2.lookup(ip_address)
    except Exception:
        def get_geo(ip_address: str) -> Any: #pylint: disable=unused-argument
            return None

    try:
        CURSOR.execute('SELECT * FROM logs')
        print('\n'.join([f'{datetime},{get_geo(ip)}' for (datetime, ip) in CURSOR.fetchall()]))
    except OperationalError:
        create_tables()
