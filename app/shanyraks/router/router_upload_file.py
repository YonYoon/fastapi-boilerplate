from typing import List

from fastapi import Depends, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

from app.auth.router.errors import InvalidCredentialsException


@router.post("/{shanyrak_id:str}/media")
def upload_files(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if str(shanyrak['user_id']) != jwt_data.user_id:
        raise InvalidCredentialsException

    result = []
    for file in files:
        url = svc.s3_service.upload_file(shanyrak_id, file.file, file.filename)
        result.append(url)
    svc.repository.add_media(result, shanyrak_id)
    return {"msg": "OK"}
