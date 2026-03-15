from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource
from pydantic import HttpUrl, SecretStr, field_validator, Field
from pathlib import Path

from delivery_s3_temporary_links.core.paths import get_file_path
from delivery_s3_temporary_links.schemas.config_schema import User, Bucket


class ModelConfig(BaseSettings):
    """Модель конфигурации"""

    model_config = SettingsConfigDict(
        env_file=get_file_path(file_name='.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )


class Config(BaseSettings):
    """Модель конфига"""

    users: list[User]
    buckets: list[Bucket]

    model_config = SettingsConfigDict(
        extra='ignore'
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            YamlConfigSettingsSource(
                settings_cls,
                yaml_file=get_file_path('config.yml'),
                yaml_file_encoding='utf-8',
            ),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class SettingsS3(ModelConfig):
    """Настройки для s3"""

    s3_endpoint: HttpUrl
    access_key: SecretStr
    secret_key: SecretStr
    sert_path_s3: str
    expires_in: int

    @field_validator('sert_path_s3')
    @classmethod
    def is_cert(cls, sert_path: str) -> str:
        """Валидатор для файла сертификата"""

        if not Path(sert_path).is_file():
            raise ValueError(f'Файл {sert_path} не обнаружен!')
        return sert_path


class SettingsApp(ModelConfig):
    """Настройки для App"""

    ip_app: str
    port_app: int
    interface: str
    workers: int
    secret: SecretStr
    allowed_hosts: str

    @property
    def ip(self) -> str:
        """Получает ip адрес"""

        return str(self.ip_app)

    @property
    def get_domains(self) -> list[str]:
        """Получает список разрешённых доменов"""

        return self.allowed_hosts.split(', ')


class SettingsRedis(ModelConfig):
    """Настройки Redis"""

    ip_redis: str
    port_redis: int
    decode_responses: bool
    prefix: str
    redis_user: str
    redis_passwd: SecretStr
    token_ttl_seconds: int

    @property
    def url_redis(self) -> str:
        """Получает url redis"""

        return f'redis://{self.redis_user}:{self.redis_passwd.get_secret_value()}@{str(self.ip_redis)}:{self.port_redis}'


class Settings(ModelConfig):
    """Класс для данных конфига"""

    settings_s3: SettingsS3 = Field(default_factory=SettingsS3)
    settings_app: SettingsApp = Field(default_factory=SettingsApp)
    settings_redis: SettingsRedis = Field(default_factory=SettingsRedis)


settings = Settings()
config = Config()  # type: ignore[missing-argument]
