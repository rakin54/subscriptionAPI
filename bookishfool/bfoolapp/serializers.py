from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
# from .models import Post

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration']


class SubscribtionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    # user_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(),
    #     source='user',
    #     write_only=True
    # )
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        source='plan',
        write_only=True
    )

    class Meta:
        model = Subscribtion
        fields = [
            'id', 'start_date', 'end_date', 'status', 'user', 'plan', 'plan_id'
        ]

    def create(self, validated_data):
        # Automatically set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)




class ExchangeRateLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRateLog
        fields = [
            'id',
            'base_currency',
            'target_currency',
            'rate',
            'fetched_at'
        ]
