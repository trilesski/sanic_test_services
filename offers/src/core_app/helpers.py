import logging
import os
import time

import psycopg2 as pg
from psycopg2 import sql, extras

from core_app.massage_const import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


def postgres_conn():
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'dev')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'devuser')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'T0x95ZXtK4')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')

    conn_wait = 0
    while True:
        try:
            conn = pg.connect(dbname=POSTGRES_DB, user=POSTGRES_USER,
                                    password=POSTGRES_PASSWORD, host=POSTGRES_HOST, connect_timeout=3)
            return conn
        except:
            time.sleep(60)
            conn_wait += 60
            logger.error(traceback.format_exc())
            logger.info(f'conn_wait {conn_wait}')


async def insert_data(table_name, data):
    col = ', '.join(data.keys())
    val = [(x,) for x in data.values()]
    with postgres_conn() as conn:
        with conn.cursor() as cursor:
            query = sql.SQL(f'INSERT INTO "{table_name}"({col}) VALUES (%s)')
            extras.execute_values(cursor, query, val)
            conn.commit()


async def select_data(table_name, fields, where_col, val):
    fields = ', '.join(fields) if len(fields) > 1 else fields[0]
    with postgres_conn() as conn:
        with conn.cursor(cursor_factory=pg.extras.RealDictCursor) as cursor:
            cursor.execute(f'''SELECT {fields} FROM "{table_name}" WHERE {where_col} = '{val}';''')
            records = cursor.fetchall()
        return records


async def validation_request(valid_keys, req):
    for x in valid_keys:
        if x[0] not in req.keys():
            VALUE_ERR['massage'] = f'Не найден ключ: {x}'
            return VALUE_ERR, 405
        else:
            if type(req[x[0]]) != x[1]:
                VALUE_ERR['massage'] = f'Передан некорректный тип данных в поле: {x[0]}'
                return VALUE_ERR, 405

    for k in req.keys():
        if k not in [x[0] for x in valid_keys]:
            VALUE_ERR['massage'] = f'Некорректный ключ: {k}'
            return VALUE_ERR, 405
    return None, None