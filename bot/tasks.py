from KGBot.celery import app


@app.task
def workspace_supervisor():
    """General task for starting grab tasks for workspaces. """
    pass


@app.task
def load_history():
    """Task for first time grab. """
    pass


@app.task
def load_latest_messages():
    """Task for loading latest messages. """
    pass
