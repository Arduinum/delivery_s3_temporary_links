from fastapi import FastAPI

from delivery_s3_temporary_links.routes.links_s3 import file_s3_router
from delivery_s3_temporary_links.routes.auth import auth_router

app = FastAPI()

app.include_router(file_s3_router)
app.include_router(auth_router)
