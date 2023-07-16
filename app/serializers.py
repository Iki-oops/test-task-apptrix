from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from .models import Client


class ClientPostSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    confirm_password = serializers.CharField()

    class Meta:
        model = Client
        fields = (
            'email',
            'first_name',
            'last_name',
            'sex',
            'avatar',
            'password',
            'confirm_password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'sex': {'required': True},
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('password') != data.pop('confirm_password'):
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def create(self, validated_data):
        client = Client(
            email=validated_data.pop('email'),
            first_name=validated_data.pop('first_name'),
            last_name=validated_data.pop('last_name'),
            sex=validated_data.pop('sex'),
            avatar=validated_data.pop('avatar'),
        )
        client.set_password(validated_data.pop('password'))
        client.save()
        return client


class ClientSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'sex',
            'avatar',
        )

    def get_avatar(self, obj):
        return '/media/' + obj.avatar.name
