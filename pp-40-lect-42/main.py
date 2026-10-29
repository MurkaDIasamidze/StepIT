from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.order_items import router as order_router
from routes.user import router as user_router
from routes.product import router as product_router

app = FastAPI(title="Shop API")

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(user_router)
app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Shop API"}
