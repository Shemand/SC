from backend.src.sc_repositories.DatabaseRepository import DatabaseRepository
from backend.src.sc_repositories.InteractionRepository import InteractionRepository
from backend.src.sc_repositories.StorageRepository import StorageRepository


class ServiceAbstract:
    def __init__(self, repositories: [InteractionRepository],
                 db: DatabaseRepository):
        self.repos = repositories
        self.db = db
