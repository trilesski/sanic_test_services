import logging
import traceback
import jwt

from core_app.helpers import *
from core_app.massage_const import *

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


async def user_reg(data):
    valid_keys = (('username', str), ('password', str), ('email', str))
    msg, st = await validation_request(valid_keys, data)
    if msg:
        return msg, st

    try:
        await insert_data(table_name='users', data=data)
    except pg.errors.UniqueViolation:
        logger.info(f"Duplicate key value: INPUT DATA: {data}")
        return DUPLICATE_VALUE, 400
    except:
        logger.error(f"Insert data to DB {data}")
        logger.error(f"{traceback.format_exc()}")
        return INSERT_DB_ERR, 500
    return INSERT_DB_SUCCESS, 201


async def user_auth(data):
    valid_keys = (('username', str), ('password', str))
    msg, st = await validation_request(valid_keys, data)
    if msg:
        return msg, st
    try:
        records = await select_data(table_name='users', fields=['id', 'username', 'password'],
                              where_col='username', val=data['username'])
    except:
        logger.error(f"Select data to DB {data['username']}")
        logger.error(f"{traceback.format_exc()}")
        return INSERT_DB_ERR, 500

    if not records:
        return INCORRECT_USERNAME, 401

    if data['password'] != records[2]:
        return INCORRECT_PASS, 401

    token = jwt.encode({'id': records[0], 'username': records[1], 'password': records[2]},
                       'secret', algorithm='HS256')
    return {'user_id': records[0], 'token': token.decode("utf-8")}, 200


async def get_users(user_id):
    try:
        records = await select_data(table_name='users', fields=['*'], where_col='id', val=user_id)
    except:
        logger.error(f"Select data to DB {user_id}")
        logger.error(f"{traceback.format_exc()}")
        return INSERT_DB_ERR, 500
    return records, 200