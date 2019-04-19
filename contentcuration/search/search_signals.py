from django.contrib.auth.models import User
from django.db import models
from contentcuration.models import ContentNode, Channel
from celery_haystack import signals
from .search_indexes import actively_indexed_models

class StudioSignalProcessor(signals.CelerySignalProcessor):
    def setup(self):
        for model in actively_indexed_models:
            models.signals.post_save.connect(self.enqueue_save, sender=model)
            models.signals.post_delete.connect(self.enqueue_delete, sender=model)

    def teardown(self):
        for model in actively_indexed_models    :
            models.signals.post_save.disconnect(self.enqueue_save, sender=model)
            models.signals.post_delete.disconnect(self.enqueue_delete, sender=model)
