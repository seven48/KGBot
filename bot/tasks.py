from bot.core.load_history import LoadHistory
from bot.core.last_messages_parser import LastMessagesParser
from KGBot.celery import app


@app.task
def workspace_supervisor():
    from bot.models import Workspace, Message
    workspaces = Workspace.objects.all()
    messages = []
    for workspace in workspaces:
        parser = LastMessagesParser(workspace=workspace)
        messages += [
            Message(**message) for message in parser.parse_channels()
        ]
    Message.objects.bulk_create(messages)


@app.task
def load_history(pk):
    """Task for first time grab. """
    from bot.models import Message, Workspace

    workspace = Workspace.objects.get(id=pk)

    for channel in workspace.channels.all():
        parser = LoadHistory(workspace)
        history = parser.load_history(workspace)
        messages_obj = [
            Message(**message) for message in history
        ]
        Message.objects.bulk_create(messages_obj)
