from functools import lru_cache
import boto3
from botocore.client import BaseClient


from delivery_s3_temporary_links.core.settings import settings


class ClientS3:
    """Класс для управления подключением к s3."""

    def __init__(self) -> None:
        self._s3_client = boto3.client(
            's3',
            endpoint_url=str(settings.settings_s3.s3_endpoint),
            aws_access_key_id=settings.settings_s3.access_key.get_secret_value(),
            aws_secret_access_key=settings.settings_s3.secret_key.get_secret_value(),
            verify=settings.settings_s3.sert_path_s3
        )

    @property
    def s3_client(self) -> BaseClient:
        """Получает клиент s3"""

        return self._s3_client


@lru_cache(maxsize=1)
def get_s3_client_instance() -> ClientS3:
    """Возвращает один и тот же объект ClientS3"""

    return ClientS3()
