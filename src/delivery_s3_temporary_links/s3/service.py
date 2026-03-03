from fastapi import status

from delivery_s3_temporary_links.s3.client import get_s3_client_instance


def get_temporary_link(bucket_name: str, key: str, expires_in: int) -> dict[str , int | str]:
    """Функция получает временную ссылку для GET запроса на файл"""

    client_s3 = get_s3_client_instance().s3_client
    temporary_link = client_s3.generate_presigned_url(
        Params={'Bucket': bucket_name, 'Key': key},
        ClientMethod='get_object',
        HttpMethod='GET',
        ExpiresIn=expires_in
    )
    return {'link': temporary_link, 'status_code': status.HTTP_200_OK}
