from typing import Any, List

from fastapi import Depends
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetFavouritesResponse(AppModel):
    id: Any = Field(alias="shanyrak_id")
    address: str


@router.get("/users/favorites/shanyraks", response_model=List[GetFavouritesResponse])
def get_favourites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> List[GetFavouritesResponse]:
    favourites = svc.favourite_repository.get_favourites(jwt_data.user_id)
    return [GetFavouritesResponse(**favourite) for favourite in favourites]