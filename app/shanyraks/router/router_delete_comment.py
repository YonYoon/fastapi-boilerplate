from fastapi import Depends

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.auth.router.errors import InvalidCredentialsException

from ..service import Service, get_service
from . import router


@router.delete("/{shanyrak_id:str}/comments/{comment_id:str}")
def delete_comment(
    comment_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    comments = svc.repository.get_comment(comment_id)
    if comments is None or len(comments) == 0:
        raise Exception("Comment not found")

    comment = None
    for c in comments:
        if str(c["_id"]) == comment_id:
            comment = c
            break

    if comment is None or str(comment["author_id"]) != jwt_data.user_id:
        raise InvalidCredentialsException

    svc.repository.delete_comment(comment_id)
    return {"msg": "OK"}
