from bot.core.load_history import LoadHistory
from KGBot.celery import app


@app.task
def workspace_supervisor():
    """General task for starting grab tasks for workspaces. """
    pass


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


@app.task
def load_latest_messages():
    """Task for loading latest messages. """
    pass
