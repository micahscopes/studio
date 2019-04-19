from haystack import indexes
from contentcuration.models import ContentNode, Channel
from celery_haystack.indexes import CelerySearchIndex
import fields

actively_indexed_models = [ContentNode, Channel]

class ContentNodeIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    title = indexes.NgramField(model_attr='title')
    channel_id = fields.ChannelIdField(model_attr='get_channel', faceted=True)
    content_kind = indexes.CharField(model_attr='kind__kind', faceted=True)
    published = indexes.BooleanField(model_attr='published', faceted=True)
    language = indexes.MultiValueField(faceted=True)

    channel_editors = indexes.MultiValueField(faceted=True)

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

    def prepare_language(self, obj):
        lang = obj.language
        return [
            lang.lang_code,
            lang.lang_subcode,
            lang.readable_name,
            lang.native_name,
            lang.lang_direction,
            lang.ietf_name()
        ] if lang else []


class ChannelIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    name = indexes.NgramField(model_attr='name')
    public = indexes.BooleanField(model_attr='public', faceted=True)
    language = indexes.MultiValueField(faceted=True)

    channel_editors = indexes.MultiValueField(faceted=True)
    # channel_name = indexes.CharField()

    def get_model(self):
        return Channel

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_channel_editors(self, obj):
        channel = obj
        if channel:
            return [str(ed.id) for ed in channel.editors.all()]
        else:
            return []

    def prepare_language(self, obj):
        lang = obj.language
        return [
            lang.lang_code,
            lang.lang_subcode,
            lang.readable_name,
            lang.native_name,
            lang.lang_direction,
            lang.ietf_name()
        ] if lang else []


