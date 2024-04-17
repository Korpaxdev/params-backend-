from datetime import timedelta

from django.utils import timezone

from backend.models import SyncLoggingModel
from users.models import UserModel


def get_sync_logger(user: UserModel) -> SyncLoggingModel:
    """Создание SyncLoggingModel для пользователя user.
    Важно! Создание модели происходит в интервал 1 минуту,
    т.е. если у пользователя в течение минуты будет еще изменение, то возьмется существующий логер
    """
    sync_logger = SyncLoggingModel.objects.filter(date__gte=timezone.now() - timedelta(minutes=1), user=user).first()
    if not sync_logger:
        sync_logger = SyncLoggingModel.objects.create(user=user)
    return sync_logger
