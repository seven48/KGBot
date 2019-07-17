from django.db import models

from bot.tasks import load_history


class Channel(models.Model):
    """Channel database model."""

    name = models.TextField(
        verbose_name='The name of Slack channel.',
        blank=False,
        null=False
    )


class Workspace(models.Model):
    """Workspaces database model."""

    url = models.TextField(
        verbose_name='Full url of Slack workspace.',
        blank=False,
        null=False
    )
    username = models.TextField(
        verbose_name='Slack workspace username.',
        blank=False,
        null=False
    )
    password = models.TextField(
        verbose_name='Slack workspace password.',
        blank=False,
        null=False
    )
    channels = models.ManyToManyField(
        Channel,
        verbose_name='Slack channels for watching.',
        blank=False,
        null=False
    )
    in_progress = models.BooleanField(
        verbose_name='Flag workspace is busy by parser.',
        default=True,
        blank=False,
        null=False
    )

    def save(self):
        if not self.id:
            super().save()
            load_history.delay(self.id)
        else:
            super().save()


class Message(models.Model):
    """Messages database model."""

    author = models.TextField(
        verbose_name='Name of user who posted the message.',
        blank=False,
        null=False
    )
    datetime = models.DateTimeField(
        verbose_name='Date and time when message posted.',
        blank=False,
        null=False
    )
    text = models.TextField(
        verbose_name='Message text.',
        blank=False,
        null=False
    )
    link = models.TextField(
        verbose_name='Unique message link.',
        blank=False,
        null=False,
        unique=True
    )
