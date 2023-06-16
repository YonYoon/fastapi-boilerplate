from fastapi import Depends

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

from app.auth.router.errors import InvalidCredentialsException


@router.delete("/{shanyrak_id:str}/media")
def delete_files(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if str(shanyrak['user_id']) != jwt_data.user_id:
        raise InvalidCredentialsException

    svc.repository.delete_media(shanyrak_id)
    return {"msg": "OK"}
