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
        res = super().to_representation(data)
        return res


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "first_name",
            "last_name",
            "email",
        )

    def to_representation(self, data):
        res = super().to_representation(data)
        return res


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_id",)

    def to_representation(self, data):
        res = super().to_representation(data)
        return res


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)

    def to_representation(self, data):
        res = super().to_representation(data)
        return res


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
