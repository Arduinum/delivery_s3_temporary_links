from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from delivery_s3_temporary_links.auth.redis_client import get_redis_client_instance
from delivery_s3_temporary_links.core.settings import settings


bearer = HTTPBearer(auto_error=False)


async def require_redis_token(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
    """Проверит есть ли токен в редис и если есть вернёт его"""

    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing token')

    token = creds.credentials
    redis_obj = get_redis_client_instance()
    user_id = await redis_obj.redis_client.get(f'{settings.settings_redis.prefix}:token:{token}')

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    return user_id
