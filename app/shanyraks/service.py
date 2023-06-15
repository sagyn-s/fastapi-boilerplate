from app.config import database

from .adapters.s3_service import S3Service
from .repository.comments_repository import CommentRepository
from .repository.repository import ShanyrakRepository


class Service:
    def __init__(
        self,
        repository: ShanyrakRepository,
    ):
        self.repository = repository
        self.s3_service = S3Service()
        self.comment_repository = CommentRepository(database)


def get_service():
    repository = ShanyrakRepository(database)
    return Service(repository)
