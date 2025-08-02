from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
import json
from datetime import datetime, timedelta
import requests
from bookishfool.settings import API_KEY
from .serializers import *
from .models import *
# Create your views here.


def index(request):
    subscribtions = Subscribtion.objects.all().order_by('-id')
    return render(request, 'index.html',{
        "subscribtions": subscribtions
    })


class RegisterView(APIView):
    
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SubscribtionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.user.is_authenticated:
                serializer = SubscribtionSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SubscribrionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.is_authenticated:
                subscriptions = Subscribtion.objects.filter(user=request.user)
                serializer = SubscribtionSerializer(subscriptions, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CancelSubscribtionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.user.is_authenticated:
                
                subscription = Subscribtion.objects.get(status="active", user=request.user)
                subscription.status = "cancelled"
                subscription.save()
                serializer = SubscribtionSerializer(subscription)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Subscribtion.DoesNotExist:
            return Response({'error': 'No Active Subscribtion Found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ExchangeRateView(APIView):
    def get_data(self, base_currency, target_currency):
        api_key = API_KEY
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
        response = requests.get(url)
        dataset = response.json()
        data = {
            "base_currency": dataset['base_code'],
            "target_currency": dataset['target_code'],
            "fetched_at": dataset['time_last_update_utc'],
            "rate": dataset['conversion_rate']
        }
        return data

    def get(self, request):
        try:
            base_currency = request.query_params.get('base')
            target_currency = request.query_params.get('target')

            base_currency = base_currency.upper()
            target_currency = target_currency.upper()

            if not base_currency or not target_currency:
                return Response(
                    {'error': 'Both base_currency and target_currency parameters are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(base_currency) != 3 or len(target_currency) != 3:
                return Response(
                   {'error': 'Currency codes must be 3 characters long'},
                   status=status.HTTP_400_BAD_REQUEST
               )

            data = self.get_data(base_currency, target_currency)
            # if data:
            return Response(data,status=status.HTTP_200_OK)
            # else:
            #     return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

