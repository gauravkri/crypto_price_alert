from rest_framework import serializers
from .models import Alert
from django.contrib.auth.models import User




class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'coin_id', 'alert_name', 'alert_price', 'status', 'createdBy']


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
