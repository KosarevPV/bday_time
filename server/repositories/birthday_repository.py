from server.db.models import Birthday
from server.repositories.base_repository import Repository


class BirthdayRepository(Repository):
    model = Birthday
