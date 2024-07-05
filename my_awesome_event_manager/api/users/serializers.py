from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "first_name",
            "last_name",
            "email",
        )
        extra_kwargs = {"email": {"required": True}}

    def to_representation(self, data):
        return super().to_representation(data)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "email",
        )

    def to_representation(self, data):
        return super().to_representation(data)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
