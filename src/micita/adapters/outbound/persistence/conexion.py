import os
import sqlite3

from micita import config


def _dict_factory(cursor, fila):
    return {col[0]: fila[i] for i, col in enumerate(cursor.description)}


def get_conn():
    conn = sqlite3.connect(config.DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = _dict_factory
    return conn


def inicializar():
    if not os.path.exists(config.DB_PATH):
        conn = get_conn()
        with open(config.DB_SCRIPT, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
    os.chmod(config.DB_PATH, 0o666)


def consultar(sql):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    filas = cur.fetchall()
    conn.close()
    return filas


def ejecutar(sql):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    except:
        pass
    finally:
        conn.close()
