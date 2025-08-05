from celery import shared_task
import requests
from django.utils import timezone
from django.conf import settings
from .models import ExchangeRateLog

@shared_task(bind=True)
def fetch_exchange_rates(self):
    api_key = settings.EXCHANGE_RATE_API_KEY
    results = []

    url = f"https://api.exchangerate-api.com/v6/{api_key}/pair/USD/BDT"
    try:
        response = requests.get(url)
        data = response.json()
            
        # Save to database
        ExchangeRateLog.objects.create(
            base_currency='USD',
            target_currency='BDT',
            rate=data['rate'],
            fetched_at=timezone.now()
        )
        results.append(f"USD-BDT: {data['rate']}")
    except Exception as e:
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds if failed

    return results