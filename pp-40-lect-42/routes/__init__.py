from routes.auth import router as auth_router
from routes.order_items import router as order_router
from routes.user import router as user_router
from routes.product import router as product_router

__all__ = ["auth_router", "order_router", "user_router", "product_router"]
