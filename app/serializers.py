from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from .models import Client, Match


class ClientPostSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = (
            'email',
            'first_name',
            'last_name',
            'sex',
            'avatar',
            'longitude',
            'latitude',
            'password',
            'confirm_password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'sex': {'required': True},
            'longitude': {'required': False},
            'latitude': {'required': False},
            'password': {'write_only': True},
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
            longitude=validated_data.pop('longitude'),
            latitude=validated_data.pop('latitude'),
        )
        client.set_password(validated_data.pop('password'))
        client.save()
        return client


class ClientLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = Client
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True}
        }


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
