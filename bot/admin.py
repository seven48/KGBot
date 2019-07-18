from django.contrib import admin

from bot.models import Channel, Message, Workspace

admin.site.register(Channel)
admin.site.register(Workspace)
admin.site.register(Message)
