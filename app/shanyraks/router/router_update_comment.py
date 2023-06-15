import imghdr
from typing import Any, List

from fastapi import Depends, HTTPException, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("/{shanyrak_id:str}/comments/{comment_id:str}")
def update_shanyrak(
    shanyrak_id: str,
    comment_id: str,
    input: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    update_result = svc.comment_repository.update_comment_by_id(comment_id, jwt_data.user_id, input.dict())
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)