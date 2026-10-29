from fastapi import HTTPException, status

from models.order import Order
from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from schemas.order import OrderCreate


class OrderService:

    def __init__(self, repository: OrderRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    async def get_all_orders(self):
        """ logika """

        return await self.repository.get_all()

    async def get_order(self, order_id: int):
        order = await self.repository.get_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {order_id} not found")
        return order

    async def create_order(self, order_data: OrderCreate):
        user = await self.user_repository.get_by_id(order_data.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user} not found")

        return await self.repository.create(user_id=order_data.user_id, total=order_data.total)
