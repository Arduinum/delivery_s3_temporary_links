from fastapi import Request, HTTPException, status
from botocore.exceptions import ClientError, ParamValidationError, BotoCoreError


async def handle_exceptions_s3(request: Request):
    """Обработчик ошибок для s3"""

    try:
        yield
    except ParamValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid parameters')
    except ClientError as err:
        code = err.response.get('Error', {}).get('Code', '')
        http = err.response.get('ResponseMetadata', {}).get('HTTPStatusCode')

        if code in {'NoSuchKey', 'NotFound'} or http == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File or folder not found')

        if code in {'AccessDenied', 'Forbidden'} or http == status.HTTP_403_FORBIDDEN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'S3 error: {code or "Unknown"}')
    except BotoCoreError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')
