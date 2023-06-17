from fastapi import Depends, HTTPException, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ...utils import AppModel
from ..service import Service, get_service
from . import router


@router.post("/users/favorites/shanyraks/{shanyraks_id:str}")
def add_to_favourite(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    user_id = jwt_data.user_id
    svc.favourite_repository.add_to_favourite(id, user_id)
    return Response(status_code=200)
