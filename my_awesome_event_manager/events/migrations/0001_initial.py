# Generated by Django 4.2.13 on 2024-07-01 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organizer', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['-created_at'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_participant_id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event Participant',
                'verbose_name_plural': 'Event Participants',
                'ordering': ['-id'],
                'managed': True,
            },
        ),
    ]