import asyncio
import logging

from sanic import Sanic
from sanic import response

from core_app.core import *

app = Sanic(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")


@app.route(methods=['POST'], uri='/user/registry')
async def run_registry_user(request):
    req_data = request.json
    result, status = await user_reg(req_data)
    return response.json(result, status=status)


@app.route(methods=['POST'], uri='/user/auth')
async def run_auth_user(request):
    req_data = request.json
    result, status = await user_auth(req_data)
    return response.json(result, status=status)


@app.route('/user/<user_id>')
async def run_get_users(request, user_id):
    result, status = await get_users(user_id)
    return response.json(result, status=status)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    srv_coro = app.create_server(host='0.0.0.0', port=8070, return_asyncio_server=True,
                                 asyncio_server_kwargs=dict(start_serving=False))
    srv = loop.run_until_complete(srv_coro)
    try:
        assert srv.is_serving() is False
        loop.run_until_complete(srv.start_serving())
        assert srv.is_serving() is True
        loop.run_until_complete(srv.serve_forever())
    except KeyboardInterrupt:
        srv.close()
        loop.close()