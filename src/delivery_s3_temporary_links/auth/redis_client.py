import redis.asyncio as aioredis
from redis.asyncio.client import Redis
from functools import lru_cache

from delivery_s3_temporary_links.core.settings import settings


class ClientRedis:
    """Класс для управления подключением к Redis."""

    def __init__(self) -> None:
        self._redis_client = aioredis.from_url(
            settings.settings_redis.url_redis,
            decode_responses=settings.settings_redis.decode_responses
        )

    @property
    def redis_client(self) -> Redis:
        """Получает клиент redis"""

        return self._redis_client


@lru_cache(maxsize=1)
def get_redis_client_instance() -> ClientRedis:
    """Возвращает один и тот же объект ClientRedis"""

    return ClientRedis()
