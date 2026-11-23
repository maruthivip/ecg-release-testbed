from aiohttp import web


async def get_order(request: web.Request) -> web.Response:
    return web.Response(text=request.match_info["order_id"])


app = web.Application()
app.router.add_get("/release/orders/{order_id}", get_order)
