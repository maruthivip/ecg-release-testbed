from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def get_order(request):
    return PlainTextResponse(request.path_params["order_id"])


app = Starlette(routes=[Route("/release/orders/{order_id}", get_order)])
