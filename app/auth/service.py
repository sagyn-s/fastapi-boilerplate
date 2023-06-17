from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .adapters.s3_service import S3Service
from .repository.favourites_repository import FavouritesRepository
from .repository.repository import AuthRepository


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = AuthConfig()


class Service:
    def __init__(
        self,
        repository: AuthRepository,
        jwt_svc: JwtService,
    ):
        self.s3_service = S3Service()
        self.favourite_repository = FavouritesRepository(database)
        self.repository = repository
        self.jwt_svc = jwt_svc


def get_service():
    repository = AuthRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)

    svc = Service(repository, jwt_svc)
    return svc
