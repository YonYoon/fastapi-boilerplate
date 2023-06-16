from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.auth.router.errors import InvalidCredentialsException
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{shanyrak_id}/comments/{comment_id:str}")
def update_comment(
    comment_id: str,
    shanyrak_id: str,
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    comment = svc.repository.get_comment(comment_id)

    if str(comment[0]["author_id"]) != jwt_data.user_id:
        raise InvalidCredentialsException

    updated_comment = svc.repository.update_comment(comment_id, jwt_data.user_id, input)
    if updated_comment.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
