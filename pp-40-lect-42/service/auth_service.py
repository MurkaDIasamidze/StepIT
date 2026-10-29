from fastapi import HTTPException, status

from core.security import create_access_token, create_refresh_token, hash_password, verify_password

from repositories.user_repository import UserRepository
from schemas.user import TokenPair, UserCreate


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, data: UserCreate):
        existing_user = await self.user_repository.get_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        hashed = hash_password(data.password)
        return await self.user_repository.create(name=data.name, email=data.email, hashed_password=hashed)

    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email)
        password_ok = verify_password(password, user.hashed_password)

        if not user or not password_ok or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password",
                                headers={"WWW-Authenticate": "Bearer"})
        token_data = {"sub": str(user.id)}
        return TokenPair(access_token=create_access_token(token_data), refresh_token=create_refresh_token(token_data))
