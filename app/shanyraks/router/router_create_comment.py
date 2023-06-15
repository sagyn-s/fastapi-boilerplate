from fastapi import Depends, HTTPException, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ...utils import AppModel
from ..service import Service, get_service
from . import router


class CreateCommentRequest(AppModel):
    content: str


@router.post("/{id:str}/comments")
def create_comment(
    id: str,
    request: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    user_id = jwt_data.user_id
    svc.comment_repository.create_comment(shanyrak_id=id, user_id=user_id, payload=request.dict())
    return Response(status_code=200)
