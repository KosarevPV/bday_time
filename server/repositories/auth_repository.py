from server.db.models import User
from server.repositories.base_repository import Repository


class AuthRepository(Repository):
    model = User
