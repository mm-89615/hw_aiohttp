from aiohttp import web

from src.database import Session


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        result = await handler(request)
        return result
