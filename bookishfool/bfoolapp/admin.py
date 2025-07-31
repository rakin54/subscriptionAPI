from django.contrib import admin
from .models import Plan, Subscribtion, ExchangeRateLog
from django.contrib.auth.models import User


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'price', 'duration']
    search_fields = ['name']


@admin.register(Subscribtion)
class SubscribtionAdmin(admin.ModelAdmin):
    list_display = ['id','user','plan', 'start_date','end_date','status']
    search_fields = ['user','plan']
    list_filter = ['status']



@admin.register(ExchangeRateLog)
class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'base_currency', 'target_currency', 'fetched_at', 'rate']
    list_filter = ['fetched_at']
    search_fields = ['base_currency', 'target_currency', 'fetched_at', 'rate']

