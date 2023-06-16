import datetime
from bson import ObjectId
from fastapi import Depends

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service

from . import router


class CreateCommentRequest(AppModel):
    content: str


@router.post("/{shanyrak_id}/comments")
def create_comment(
    shanyrak_id: str,
    input: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    comment_id = str(ObjectId())
    time = datetime.datetime.now()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    svc.repository.add_comment(
        shanyrak_id=shanyrak_id,
        user_id=jwt_data.user_id,
        data=input.content,
        comment_id=comment_id,
        time=time_str
    )

    return {"msg": "OK"}
