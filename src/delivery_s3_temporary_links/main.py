from fastapi import FastAPI

from delivery_s3_temporary_links.routes.links_s3 import file_s3_router


app = FastAPI()

app.include_router(file_s3_router)
