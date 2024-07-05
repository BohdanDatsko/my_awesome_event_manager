from django.contrib.auth import get_user_model
from rest_framework import serializers

from my_awesome_event_manager.api.users.serializers import UserCompactSerializer
from my_awesome_event_manager.events.models import Event
from my_awesome_event_manager.events.models import EventParticipant

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventSerializer(serializers.ModelSerializer):
    organizer = UserCompactSerializer(read_only=True)
    participants = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Event
        fields = (
            "event_id",
            "title",
            "description",
            "date",
            "location",
            "organizer",
            "created_at",
            "updated_at",
            "participants",
        )
        extra_kwargs = {
            "title": {"required": True},
            "date": {"required": True},
            "location": {"required": True},
        }

    def create(self, validated_data):
        participants = validated_data.pop("participants", [])
        event = Event.objects.create(**validated_data)
        for participant in participants:
            user = User.objects.filter(email=participant).first()
            if user:
                EventParticipant.objects.create(event=event, user=user)
            else:
                EventParticipant.objects.create(event=event, email=participant)
        return event

    def to_representation(self, data):
        return super().to_representation(data)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class EventCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "event_id",
            "title",
            "location",
            "date",
            "organizer",
        )

    def to_representation(self, data):
        return super().to_representation(data)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
