from asyncio import sleep

from aiohttp import web

from src.app import app
from src.database import close_orm, init_orm
from src.utils.middlewares import session_middleware
from src.views.advertisement import AdvertisementView


async def orm_contex(app: web.Application):
    await init_orm()
    yield
    await close_orm()


app.cleanup_ctx.append(orm_contex)
app.middlewares.append(session_middleware)

app.add_routes(
    [
        web.get("/ad", AdvertisementView),
        web.get("/ad/{ad_id:[0-9]+}", AdvertisementView),
        web.post("/ad", AdvertisementView),
        web.patch("/ad/{ad_id:[0-9]+}", AdvertisementView),
        web.delete("/ad/{ad_id:[0-9]+}", AdvertisementView),
    ]
)
if __name__ == "__main__":
    web.run_app(app)
