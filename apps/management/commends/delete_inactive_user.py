# management/commands/delete_inactive_users.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.paper.models import PaperUser
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete inactive users that have not been activated after a certain period'

    def handle(self, *args, **options):
        # 设置未激活账户的保留时间阈值，例如 7 天
        inactive_period = timedelta(days=1)
        # 获取当前时间
        cutoff_date = timezone.now() - inactive_period

        # 删除超过保留时间阈值的未激活账户
        inactive_users = PaperUser.objects.filter(
            date_joined__lte=cutoff_date,
            is_active=False
        )
        inactive_users_count = inactive_users.count()
        inactive_users.delete()

        self.stdout.write(self.style.SUCCESS(
            f'用户长时间未激活已被删除: {inactive_users_count} '
        ))
