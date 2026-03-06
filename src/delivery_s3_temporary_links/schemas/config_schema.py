from pydantic import BaseModel, SecretStr, field_validator
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['sha256_crypt'])


class User(BaseModel):
    """Модель валидации для user"""

    username: str
    passwd: SecretStr

    @field_validator('passwd')
    @classmethod
    def hash_password(cls, value: SecretStr) -> SecretStr:
        raw = value.get_secret_value()

        # Если уже bcrypt — не трогаем
        if raw.startswith("$2b$"):
            return value

        hashed = pwd_context.hash(raw)
        return SecretStr(hashed)


class Folder(BaseModel):
    """Модель валидации для folder"""

    name: str
    status: str


class Bucket(BaseModel):
    """Модель валидации для bucket"""

    name: str
    folders: list[Folder]
