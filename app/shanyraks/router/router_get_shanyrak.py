from typing import Any, List

from fastapi import Depends, HTTPException, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any
    media: List[str] = []
    location: dict


@router.get("/{shanyrak_id:str}", response_model=GetShanyrakResponse)
def get_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if not shanyrak:
        raise HTTPException(status_code=404, detail=f"Could find shanyrak with id {shanyrak_id}")
    address = shanyrak["address"]
    shanyrak["location"] = svc.here_service.get_coordinates(address)
    if shanyrak is None:
        return Response(status_code=404)
    return GetShanyrakResponse(**shanyrak)
