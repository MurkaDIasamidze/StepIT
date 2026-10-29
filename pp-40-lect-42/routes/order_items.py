from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from repositories.order_repository import OrderRepository
from repositories.user_repository import UserRepository
from schemas.order import OrderResponse, OrderCreate
from service.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_order_service(db: AsyncSession = Depends(get_db)):
    return OrderService(OrderRepository(db), UserRepository(db))


@router.get("/", response_model=list[OrderResponse])
async def get_orders(service: OrderService = Depends(get_order_service)):
    return await service.get_all_orders()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    return await service.get_order(order_id)


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, service: OrderService = Depends(get_order_service)):
    return await service.create_order(order)
