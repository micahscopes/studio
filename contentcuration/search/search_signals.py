from django.contrib.auth.models import User
from django.db import models
from contentcuration.models import ContentNode, Channel
from contentcuration.signals import changed_tree, channel_updated
from celery_haystack import signals
from .search_indexing_tasks import partial_update_subtree


actively_indexed_models = [ContentNode, Channel]
class StudioSignalProcessor(signals.CelerySignalProcessor):
    def setup(self):
        for model in actively_indexed_models:
            models.signals.post_save.connect(self.enqueue_save, sender=model)
            models.signals.post_delete.connect(self.enqueue_delete, sender=model)

        changed_tree.connect(self.enqueue_update_subtree)


    def teardown(self):
        for model in actively_indexed_models:
            models.signals.post_save.disconnect(self.enqueue_save, sender=model)
            models.signals.post_delete.disconnect(self.enqueue_delete, sender=model)

    def enqueue_update_subtree(self, parent_node, fields):
        partial_update_subtree.apply_async((parent_node, fields))

    def enqueue_changed_tree(self, moved_contentnode, new_parent):
        partial_update_subtree.apply_async(())
