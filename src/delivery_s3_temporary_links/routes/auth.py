from fastapi import APIRouter, HTTPException, status
import jwt
from datetime import timezone, timedelta, datetime
from redis.exceptions import RedisError

from delivery_s3_temporary_links.core.settings import settings, config
from delivery_s3_temporary_links.auth.redis_client import get_redis_client_instance
from delivery_s3_temporary_links.schemas.config_schema import pwd_context


auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/login')
async def login(username: str, password: str):
    """Логинит юзера в систему"""

    hashed = None

    for user in config.users:
        if user.username == username:
            hashed = user.passwd.get_secret_value()
            break

    if not hashed or not pwd_context.verify(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    token = jwt.encode(
        {
            'sub': username,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=settings.settings_redis.token_ttl_seconds)
        },
        settings.settings_app.secret.get_secret_value(),
        algorithm='HS256'
    )

    try:
        redis = get_redis_client_instance()
        await redis.redis_client.set(f'{settings.settings_redis.prefix}:token:{token}', username, ex=settings.settings_redis.token_ttl_seconds)
    except RedisError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error Server')

    return {'access_token': token}
