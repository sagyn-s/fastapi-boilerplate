import imghdr
from typing import Any, List

from fastapi import Depends, HTTPException, Response, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class UpdateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{shanyrak_id:str}")
def update_shanyrak(
    shanyrak_id: str,
    input: UpdateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    update_result = svc.repository.update_shanyrak(shanyrak_id, jwt_data.user_id, input.dict())
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)


@router.post("/{shanyrak_id:str}/media")
def update_shanyrak_photos(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    media = []
    for file in files:
        if not is_image(file.file.read()):
            raise HTTPException(status_code=400, detail=f"{file.filename} is not an image")
        url = svc.s3_service.upload_file(file.file, file.filename)
        media.append(url)
    svc.repository.update_shanyrak(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id, data={"media": media})
    return media
#648af5359e4dedf63e49c829


@router.delete("/{shanyrak_id:str}/media")
def update_shanyrak_photos(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Any:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id=shanyrak_id)
    media = shanyrak.get("media", [])
    for url in media:
        svc.s3_service.delete_file(url.split("/")[-1])
    svc.repository.update_shanyrak(shanyrak_id=shanyrak_id, user_id=jwt_data.user_id, data={"media": []})
    return media


def is_image(file_contents: bytes) -> bool:
    image_type = imghdr.what(None, file_contents)
    return image_type is not None
