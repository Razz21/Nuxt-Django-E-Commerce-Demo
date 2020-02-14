from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .utils import format_expiry_datetime

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """

    token = serializers.SerializerMethodField()
    expiry = serializers.SerializerMethodField()
    # user = UserSerializer()

    def get_token(self, obj):
        return obj["token"][1]

    def get_expiry(self, obj):
        return format_expiry_datetime(obj["token"][0].expiry)
