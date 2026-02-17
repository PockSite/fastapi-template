from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError as e:
        print(f"Token verification failed: {e}")
        return None

