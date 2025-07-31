from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
import requests
from bookishfool.settings import API_KEY
from .serializers import *
from .models import *
# Create your views here.


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
    

class ExchangeRateView(APIView):
    def get_data(self, base_currency, target_currency):
        api_key = API_KEY
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
        response = requests.get(url)
        data = response.json()
        return data['data'][target_currency]

    def get(self,request):
        try:
            exchange_rate = self.get_data("USD", "DBT")
            return Response({'exchange_rate': exchange_rate})
        # serializers = ExchangeRateLogSerializer(data=request.data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

