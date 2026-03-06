from delivery_s3_temporary_links.schemas.config_schema import Folder, Bucket


def is_status_folder(buckets: list[Bucket], bucket_name: str, folder: str, status: str) -> bool:
    """Функция определяет bool статуса папки"""

    search_folder = None

    for bucket in buckets:
        if bucket.name == bucket_name:
            search_folder = next((folder_obj for folder_obj in bucket.folders if folder_obj.name == folder), None)
            break

    return isinstance(search_folder, Folder) and search_folder.status == status
