from fastapi import HTTPException, status
from repositories.product_repository import ProductRepository
from schemas.product import ProductCreate


class ProductService:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_all_product(self):
        """ logika """

        return await self.repository.get_all()

    async def get_product(self, product_id: int):
        product = await self.repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product} not found")
        return product

    async def create_product(self, product_data: ProductCreate):
        return await self.repository.create(
            name=product_data.name,
            price=product_data.price,
            description=product_data.description
        )
