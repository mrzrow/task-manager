from fastapi import APIRouter, Depends, HTTPException
from app.services.user import UserService
from app.depends.user import get_user_service
from app.schemas.user import (
    UserCreate,
    UserBase,
    UserUpdate,
    UserGetById,
    UserDelete
)


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/', response_model=list[UserBase])
async def get_users(
    service: UserService = Depends(get_user_service) 
) -> list[UserBase]:
    try:
        return await service.get_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{user_id}', response_model=UserBase)
async def get_user_by_id(
    user_id: int, 
    service: UserService = Depends(get_user_service) 
) -> UserBase:
    try:
        user_in = UserGetById(id=user_id)
        user = await service.get_user_by_id(user_in)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/', response_model=UserBase)
async def create_user(
    user_create: UserCreate, 
    service: UserService = Depends(get_user_service) 
) -> UserBase:
    try:
        return await service.create_user(user_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put('/', response_model=UserBase)
async def update_user(
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> UserBase:
    try:
        return await service.update_user(user_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
) -> None:
    user_in = UserDelete(id=user_id)
    try:
        await service.delete_user(user_in)
        return {"detail": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
