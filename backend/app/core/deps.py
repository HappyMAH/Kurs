from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.models.user import UserRole

bearer_scheme = HTTPBearer()


def _get_payload(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )
    return payload


def get_current_user_id(payload: dict = Depends(_get_payload)) -> int:
    return int(payload["sub"])


def get_current_user_role(payload: dict = Depends(_get_payload)) -> UserRole:
    return UserRole(payload["role"])


def require_admin(role: UserRole = Depends(get_current_user_role)) -> None:
    if role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required",
        )
