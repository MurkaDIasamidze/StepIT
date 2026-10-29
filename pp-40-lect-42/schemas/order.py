from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    user_id: int
    total: float


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: float

    model_config = ConfigDict(from_attributes=True)
