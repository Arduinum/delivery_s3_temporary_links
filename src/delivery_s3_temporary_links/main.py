from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from delivery_s3_temporary_links.routes.links_s3 import file_s3_router
from delivery_s3_temporary_links.routes.auth import auth_router
from delivery_s3_temporary_links.core.settings import settings


app = FastAPI()

# Подключение роутеров
app.include_router(file_s3_router)
app.include_router(auth_router)

# Подключение middlewares
app.add_middleware(
    TrustedHostMiddleware,  # type: ignore
    allowed_hosts=settings.settings_app.get_domains
)
