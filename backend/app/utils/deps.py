from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config import settings
from app.models.user import UserModel
from app.models.schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token") # For documentation/testing purposes mainly

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await UserModel.find_by_id(user_id)
    if user is None:
        raise credentials_exception
        
    # Helper to convert MongoDB doc to Schema-friendly dict
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "total_stars": user.get("total_stars", 0),
        "level": user.get("level", 1),
        "created_at": user.get("created_at").isoformat() if user.get("created_at") else None
    }
