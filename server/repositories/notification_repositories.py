from server.db.models import Notification
from server.repositories.base_repository import Repository


class NotificationRepository(Repository):
    model = Notification
