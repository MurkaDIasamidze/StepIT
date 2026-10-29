from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.order import Order


class OrderRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Order))
        return list(result.scalars().all())

    async def get_by_id(self, order_id: int):
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int):
        result = await self.db.execute(select(Order).where(Order.user_id == user_id))
        return list(result.scalars().all())

    async def create(self, user_id: int, total: float):
        order = Order(user_id=user_id, total=total)
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order
