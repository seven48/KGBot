# Generated by Django 2.2.3 on 2019-07-15 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='in_progress',
            field=models.BooleanField(default=True, verbose_name='Flag workspace is busy by parser.'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.TextField(verbose_name='The name of Slack channel.'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='channels',
            field=models.ManyToManyField(to='bot.Channel', verbose_name='Slack channels for watching.'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='password',
            field=models.TextField(verbose_name='Slack workspace password.'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='url',
            field=models.TextField(verbose_name='Full url of Slack workspace.'),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='username',
            field=models.TextField(verbose_name='Slack workspace username.'),
        ),
    ]
