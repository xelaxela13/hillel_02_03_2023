from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from currencies.clients.privatbank import privatbank_client
from currencies.models import CurrencyHistory
from project.celery import app


@app.task
def delete_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(minutes=5)
    ).delete()


@shared_task
def get_currencies_task():
    privatbank_client.save()
    delete_old_currencies.delay()
