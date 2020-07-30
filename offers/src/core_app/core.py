import logging
import traceback

from core_app.helpers import *
from core_app.massage_const import *


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


async def offer_create(data):
    valid_keys = (('user_id', int), ('title', str), ('text', str))
    msg, st = await validation_request(valid_keys, data)
    if msg:
        return msg, st
    try:
        await insert_data(table_name='offers', data=data)
    except Exception:
        logger.error(f"Insert data to DB {data}")
        logger.error(f"{traceback.format_exc()}")
        return INSERT_DB_ERR, 500
    return INSERT_DB_SUCCESS, 201


async def get_offer(data):
    if 'user_id' in data.keys():
        msg, st = await validation_request((('user_id', int),), data)
    else:
        msg, st = await validation_request((('offer_id', int),), data)
    if msg:
        return msg, st
    try:
        if 'user_id' in data:
            records = await select_data(table_name='offers', fields=['*'],
                                  where_col='user_id', val=data['user_id'])
        else:
            records = await select_data(table_name='offers', fields=['*'],
                                  where_col='id', val=data['offer_id'])
        records = [dict(x) for x in records]
    except Exception:
        logger.error(f"Insert data to DB {data}")
        logger.error(f"{traceback.format_exc()}")
        return INSERT_DB_ERR, 500
    SELECT_DB_SUCCESS['values'] = records
    return SELECT_DB_SUCCESS, 200