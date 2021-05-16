from collections import OrderedDict

from django.contrib.auth import get_user_model  # If used custom user model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data.get('email', None)
        first_name = validated_data.get('first_name', '')
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=email,
            first_name=first_name,
        )

        return user

    def to_representation(self, instance):
        instance = super(UserSerializer, self).to_representation(instance)
        return OrderedDict([(key, instance[key])
                            for key in instance if key not in ['email', 'first_name']
                            or (instance[key] is not None and len(instance[key]) > 1)])

    class Meta:
        model = UserModel
        fields = ("id", "username", "password", "email", "first_name")
