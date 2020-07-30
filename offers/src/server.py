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


@app.route(methods=['POST'], uri='/offer/create')
async def run_offer_create(request):
    req_data = request.json
    result, status = await offer_create(req_data)
    return response.json(result, status=status)


@app.route(methods=['POST'], uri='/offer/')
async def run_get_offer(request):
    req_data = request.json
    result, status = await get_offer(req_data)
    return response.json(result, status=status)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    srv_coro = app.create_server(host='0.0.0.0', port=8075, return_asyncio_server=True,
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