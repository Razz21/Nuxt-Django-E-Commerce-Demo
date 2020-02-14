from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework.serializers import DateTimeField


def create_knox_token(token_model, user, serializer):
    token = AuthToken.objects.create(user=user)
    return token


def format_expiry_datetime(expiry):
    datetime_format = knox_settings.EXPIRY_DATETIME_FORMAT
    return DateTimeField(format=datetime_format).to_representation(expiry)
