import asyncio
import aiohttp_jinja2
import jinja2
import os
import aiohttp
from aiohttp import web


@aiohttp_jinja2.template('order.html')
async def index(request):
    return {'request': request}


async def price(request):
    return web.json_response(await get_price(request.GET,
                                             request.app['config']))


def get_price_value(price_value):
    return int(round(price_value * 0.2))


def get_price_string(price):
    return 'After{}: {}-{} {}'.format(price['display_name'],
                                      get_price_value(price['low_estimate']),
                                      get_price_value(price['high_estimate']),
                                      price['currency_code'])


async def get_price(locations, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(config['api_url'], params=locations,
                               headers=get_auth(config)) as resp:
            if resp.status == 200:
                result = await resp.json()
                return [get_price_string(x) for x in result['prices']]
            return []


def get_auth(config):
    return {
        'Authorization': 'Token {}'.format(config['server_token'])
    }


def get_config():
    return {
        'api_url': 'https://api.uber.com/v1/estimates/price',
        'client_id': 'v6segMoIpIuOPVZ8CPtZTqwn6QVK-1zV',
        'client_secret': 'g70zXI-qQdyb2jDdEE3m5u1clhl0a6Tf_LtbfzIw',
        'server_token': 'rXFtyR-_8FnRpknNVFkDlkb1Psi_B-bdVa2mD_Pf',
    }


def create_loop():
    return asyncio.get_event_loop()


def create_application(loop):
    app = web.Application(loop=loop)
    app['config'] = get_config()
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    tpl_dir = os.path.join(curr_dir, 'templates')
    static_dir = os.path.join(curr_dir, 'static')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(tpl_dir))

    app.router.add_get('/', index, name='index')
    app.router.add_get('/price', price, name='price')
    app.router.add_static('/static/', static_dir, name='static')
    return app


app = create_application(create_loop())


if __name__ == '__main__':
    web.run_app(app)

