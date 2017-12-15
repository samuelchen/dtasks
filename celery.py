#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, unicode_literals
from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtasks.settings')


class MyCelery(Celery):

    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super(MyCelery, self).gen_task_name(name, module)

app = MyCelery('dtasks', broker='sqla+sqlite:///dtasks.sqlite3')
app.conf.update(
    CELERY_RESULT_BACKEND='db+sqlite:///dtasks.sqlite3',
    # CELERY_RESULT_BACKEND = 'redis://localhost/0',
    #   CELERY_RESULT_BACKEND = 'amqp',
    #   CELERY_RESULT_BACKEND = 'mongodb://127.0.0.1:27017/',
    CELERY_TASK_SERIALIZER='json',
    CELERY_IGNORE_RESULT=False,
)


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
