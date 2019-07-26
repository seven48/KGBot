import time

from bot.core.load_history import LoadHistory
from bot.core.last_messages_parser import LastMessagesParser
from KGBot.celery import app
from KGBot.settings import ROCKET_CHANNEL, ROCKET_USER, ROCKET_URL, ROCKET_PASS

from rocketchat_API.rocketchat import RocketChat


def send_message_to_rocket(rocket, message, channel, delay=1):
    time.sleep(delay)
    try:
        rocket.chat_post_message(message, channel=channel)
    except:  # noqa: E722
        pass


@app.task
def workspace_supervisor():
    from bot.models import Workspace, Message
    workspaces = Workspace.objects.all()
    messages = []
    rocket = RocketChat(ROCKET_USER, ROCKET_PASS, server_url=ROCKET_URL)
    for workspace in workspaces:
        parser = LastMessagesParser(workspace=workspace)
        for channel in workspace.channels.all():
            all_last_messages = parser.get_messages(channel.name)
            for message in all_last_messages:
                send_message_to_rocket(rocket,
                                       f"{channel.name}: {message['text']}",
                                       ROCKET_CHANNEL)
            messages += [
                Message(**message) for message in all_last_messages
            ]

    Message.objects.bulk_create(messages)


@app.task
def load_history(pk):
    """Task for first time grab. """
    from bot.models import Message, Workspace

    workspace = Workspace.objects.get(id=pk)
    parser = LoadHistory(workspace)
    rocket = RocketChat(ROCKET_USER, ROCKET_PASS, server_url=ROCKET_URL)
    for channel in workspace.channels.all():
        print(channel.name)
        history = parser.load_history_v2(channel.name)
        messages_obj = [
            Message(**message) for message in history
        ]
        Message.objects.bulk_create(messages_obj)
        for message in history:
            send_message_to_rocket(rocket,
                                   f"{channel.name}: {message['text']}",
                                   ROCKET_CHANNEL)
