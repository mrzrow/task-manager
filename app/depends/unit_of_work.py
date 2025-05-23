from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.utils.unit_of_work import UnitOfWork

async def get_unit_of_work(
    session: AsyncSession = Depends(get_session)
) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(session) as uow:
        yield uow
