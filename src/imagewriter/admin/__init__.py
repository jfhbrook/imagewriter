from aiohttp import web


async def index(request: web.Request) -> web.Response:
    # Handle a web request
    return web.Response(text='{"ok":true}')


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.get("/", index)])
    return app


def admin() -> None:
    web.run_app(create_app())
