from django.contrib.auth.models import User
from django.db import models
from contentcuration.models import ContentNode, Channel
from contentcuration.signals import changed_tree, channel_updated
from .search_indexes import ContentNodeIndex, ContentNodeChannelInfo
from celery_haystack import signals
from .search_indexing_tasks import partial_update_subtree


actively_indexed_models = [ContentNode, Channel]
class StudioSignalProcessor(signals.CelerySignalProcessor):
    def setup(self):
        for model in actively_indexed_models:
            models.signals.post_save.connect(self.enqueue_save, sender=model)
            models.signals.post_delete.connect(self.enqueue_delete, sender=model)

        channel_updated.connect(self.enqueue_update_channel_tree, sender=Channel)
        changed_tree.connect(self.enqueue_changed_tree, sender=ContentNode)


    def teardown(self):
        for model in actively_indexed_models:
            models.signals.post_save.disconnect(self.enqueue_save, sender=model)
            models.signals.post_delete.disconnect(self.enqueue_delete, sender=model)

        channel_updated.disconnect(self.enqueue_update_channel_tree, sender=Channel)
        changed_tree.disconnect(self.enqueue_changed_tree, sender=ContentNode)


    def enqueue_update_channel_tree(self, channel, **kwargs):
        channel_info = ContentNodeIndex().prepare_channel_info(channel)
        partial_update_subtree.apply_async((channel.main_tree, {'channel_info': channel_info}))

    def enqueue_changed_tree(self, contentnode, **kwargs):
        channel_info = ContentNodeIndex().prepare_channel_info(contentnode)
        partial_update_subtree.apply_async((contentnode, {'channel_info': channel_info}))
