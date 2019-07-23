# KGBot
Slack message grabber with Django admin written on python

# Run workers

```celery -A bot.tasks worker --loglevel=info```

# Run beat

```celery -A bot.tasks beat --loglevel=info```
