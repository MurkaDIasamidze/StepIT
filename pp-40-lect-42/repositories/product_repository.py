from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product


class ProductRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Product))
        return list(result.scalars().all())

    async def get_by_id(self, product_id: int):
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def create(self, name: str, price: float, description: str | None = None):
        product = Product(name=name, price=price, decription=description)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
