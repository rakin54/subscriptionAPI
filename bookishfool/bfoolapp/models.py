from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price (USD)')
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='Duration (Days)')


class Subscribtion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('cancelled', 'Cancelled'), ('expired', 'Expired')])


class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    fetched_at = models.DateField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)