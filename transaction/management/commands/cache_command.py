from django.core.management import BaseCommand
from transaction.helper import cache_insert_query

class Command(BaseCommand):
    """
    This command for cache data after calculate and we can set it per hours or per day to run
    for this job wen can set on celery or OS cron job
    """
    def handle(self, *args, **options):
        cache_insert_query()