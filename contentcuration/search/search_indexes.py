from haystack import indexes
from contentcuration.models import ContentNode
from celery_haystack.indexes import CelerySearchIndex
import fields

class ContentNodeIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    title = indexes.CharField(model_attr='title')
    channel_id = fields.ChannelIdField(model_attr='get_channel', faceted=True)
    kind = indexes.CharField(model_attr='kind__kind', faceted=True)
    published = indexes.BooleanField(model_attr='published', faceted=True)

    channel_editors = indexes.MultiValueField(faceted=True)
    # channel_name = indexes.CharField()

    def get_model(self):
        return ContentNode

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_channel_editors(self, obj):
        channel = obj.get_channel()
        if channel:
            return [str(ed.id) for ed in channel.editors.all()]
        else:
            return []
