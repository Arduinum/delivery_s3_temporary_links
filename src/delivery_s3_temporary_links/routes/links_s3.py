from fastapi import Depends, status, HTTPException, APIRouter

from delivery_s3_temporary_links.s3.service import get_temporary_link
from delivery_s3_temporary_links.core.settings import settings
from delivery_s3_temporary_links.core.settings import config
from delivery_s3_temporary_links.auth.redis_bearer import require_redis_token
from delivery_s3_temporary_links.dependency.errors import handle_exceptions_s3
from delivery_s3_temporary_links.utils.utils import is_status_folder


file_s3_router = APIRouter(prefix='/files_s3', tags=['files_s3'])


@file_s3_router.get('/{bucket_name}/{folder}/private/{name}', status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_redis_token), Depends(handle_exceptions_s3)])
async def get_file_secret_link(bucket_name: str, folder: str, name: str):
    """Ручка для получения ссылки на секретный файл"""

    if is_status_folder(buckets=config.buckets, bucket_name=bucket_name, folder=folder, status='private'):
        data_link = get_temporary_link(
            bucket_name=bucket_name,
            key=f'{folder}/{name}',
            expires_in=settings.settings_s3.expires_in
        )

        return data_link

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='File or folder not found'
    )


@file_s3_router.get('/{bucket_name}/{folder}/public/{name}', status_code=status.HTTP_200_OK,
    dependencies=[Depends(handle_exceptions_s3)])
async def get_file_public_link(bucket_name: str, folder: str, name: str):
    """Ручка для получения ссылки на публичный файл"""

    if is_status_folder(buckets=config.buckets, bucket_name=bucket_name, folder=folder, status='public'):
        data_link = get_temporary_link(
            bucket_name=bucket_name,
            key=f'{folder}/{name}',
            expires_in=settings.settings_s3.expires_in
        )

        return data_link

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='File or folder not found'
    )
