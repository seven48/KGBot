from bot.core.load_history import LoadHistory
from KGBot.celery import app


@app.task
def workspace_supervisor():
    """General task for starting grab tasks for workspaces. """
    pass


@app.task
def load_history(pk):
    """Task for first time grab. """
    from bot.models import Workspace

    workspace = Workspace.objects.get(id=pk)

    LoadHistory(workspace)


@app.task
def load_latest_messages():
    """Task for loading latest messages. """
    pass
