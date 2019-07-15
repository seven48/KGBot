from django.db import models


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
