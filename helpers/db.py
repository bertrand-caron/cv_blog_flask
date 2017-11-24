from sqlite3 import connect, OperationalError
from typing import Any

DB_CONN = connect('cv.db', isolation_level=None)
CURSOR = DB_CONN.cursor()

def create_tables() -> None:
    CURSOR.execute('CREATE TABLE logs (datetime DATETIME, ip VARCHAR(39))')

def log_access(request: Any) -> None:
    print(request.environ)
    CURSOR.execute('INSERT INTO logs (datetime, ip) VALUES (DATETIME("now"), ?)', (request.environ['HTTP_X_REAL_IP'],))

if __name__ == '__main__':
    try:
        CURSOR.execute('SELECT * FROM logs')
        print(CURSOR.fetchall())
    except OperationalError:
        create_tables()
