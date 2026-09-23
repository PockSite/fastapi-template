from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_user_service
from app.schemas.user import UserRequest, UserResponse
from app.service.user_service import UserService

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserRequest, service: UserService = Depends(get_user_service)):
    return service.create_user(name=data.name, email=data.email)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserRequest, service: UserService = Depends(get_user_service)):
    user = service.update_user(user_id=user_id, name=data.name, email=data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
