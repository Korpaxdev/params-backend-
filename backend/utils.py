from datetime import timedelta

from django.utils import timezone

from backend.models import SyncLoggingModel
from users.models import UserModel


def get_sync_logger(user: UserModel) -> SyncLoggingModel:
    sync_logger = SyncLoggingModel.objects.filter(date__gte=timezone.now() - timedelta(minutes=1), user=user).first()
    if not sync_logger:
        sync_logger = SyncLoggingModel.objects.create(user=user)
    return sync_logger
