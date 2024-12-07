from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self) -> dict[str, int]:
        return {"id": self.id}
