from rest_framework import serializers

import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core import exceptions
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from .models import (Log, 
                     Origin, 
                     Environment,
                     Level)

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('title',
                  'details',
                  'number_events',
                  'occurrence_date',
                  'active',
                  'environment',
                  'level',
                  'origin',
                  'user'
                 )
        read_only_fields = ['occurrence_date', 'active']

class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = ['description']
        read_only_fields = ['description']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['description']
        read_only_fields = ['description']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def validate_password(self, data):
        try:
            validators.validate_password(data, self.instance)
        
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data
    
    def validate_email(self, data):
        users = User.objects.filter(email=data)

        if(users):
            raise serializers.ValidationError(["email must be unique"])

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        
        return user

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ['id', 'description']
        read_only_fields = ['description']
