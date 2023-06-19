from typing import Any, List, Optional

from fastapi import Depends, Query, Response
from pydantic import Field

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Shanyrak(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    location: dict


class GetShanyraksResponse(AppModel):
    total: int
    objects: List[Shanyrak]
    

@router.get("/", response_model=GetShanyraksResponse)
def get_shanyraks(
    limit: int,
    offset: int,
    type: Optional[str] = None,
    rooms_count: Optional[int] = None,
    price_from: Optional[int] = None,
    price_until: Optional[int] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: Optional[float] = None,
    svc: Service = Depends(get_service),
):
    result = svc.repository.get_shanyraks(limit, offset, type, rooms_count, price_from, price_until, latitude, longitude, radius)
    for i in range(len(result["objects"])):
        address = result["objects"][i]["address"]
        result["objects"][i]["location"] = svc.here_service.get_coordinates(address)
     
    return result
