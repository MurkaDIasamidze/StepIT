from fastapi import HTTPException, status
from repositories.user_repository import UserRepository
from schemas.user import UserCreate


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_user(self):
        """ logika """

        return await self.repository.get_all()

    async def get_user(self, user_id: int):
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user} not found")
        return user

    async def create_user(self, user_data: UserCreate):
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User with email {user_data.email}  already exists")

        return await self.repository.create(
            name=user_data.name,
            email=user_data.email
        )
