from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_user_service
from app.schemas.user import RegisterUserRequest
from app.service.user_service import UserService

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter()

@router.get("/")
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/me")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service)
):
    try:
        return service.get_current_user(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterUserRequest, 
             service: UserService = Depends(get_user_service),
             token: str = Depends(oauth2_scheme)):
    try:
        return service.register_user(data.id, data.email, data.name, token)

    except ValueError as e:
        print(f"Error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
