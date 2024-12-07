from aiohttp import web
from aiohttp.web import HTTPNotFound
from aiohttp.web_exceptions import HTTPConflict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.advertisement import Advertisement
from utils.generate_error import generate_error
from utils.validation import CreateAdvertisementSchema, UpdateAdvertisementSchema, validate_json


async def get_ad_by_id(session: AsyncSession, ad_id: int) -> Advertisement:
    ad = await session.get(Advertisement, ad_id)
    if not ad:
        raise generate_error(HTTPNotFound, f"Advertisement with id {ad_id} not found")
    return ad


async def get_ads(session: AsyncSession):
    ads = await session.execute(select(Advertisement))
    ads = ads.scalars().all()
    if not ads:
        raise generate_error(HTTPNotFound, "Advertisements not found")
    return ads


async def add_ad(session: AsyncSession, ad: Advertisement) -> Advertisement:
    session.add(ad)
    try:
        await session.commit()
    except IntegrityError:
        raise generate_error(HTTPConflict, f"Advertisement with title '{ad.title}' already exists")


class AdvertisementView(web.View):

    @property
    def ad_id(self):
        if self.request.match_info.get("ad_id"):
            return int(self.request.match_info["ad_id"])

    async def get(self):
        if self.ad_id:
            ad = await get_ad_by_id(self.request.session, self.ad_id)
            return web.json_response(ad.dict)
        ads = await get_ads(self.request.session)
        return web.json_response([ad.dict for ad in ads])

    async def post(self):
        json_data = await self.request.json()
        validate_data = validate_json(json_data, CreateAdvertisementSchema)
        ad = Advertisement(**validate_data)
        await add_ad(self.request.session, ad)
        return web.json_response(ad.id_dict)

    async def patch(self):
        json_data = await self.request.json()
        validate_data = validate_json(json_data, UpdateAdvertisementSchema)
        ad = await get_ad_by_id(self.request.session, self.ad_id)
        for key, value in validate_data.items():
            setattr(ad, key, value)
        await add_ad(self.request.session, ad)
        return web.json_response(ad.id_dict)

    async def delete(self):
        ad = await get_ad_by_id(self.request.session, self.ad_id)
        await self.request.session.delete(ad)
        await self.request.session.commit()
        return web.json_response({"status": "deleted"})
