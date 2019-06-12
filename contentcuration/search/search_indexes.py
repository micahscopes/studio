from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from .partial_update import PartiallyUpdatableIndex
from contentcuration.models import ContentNode, Channel

class ContentNodeChannelInfo(indexes.SearchIndex):
    # make sure these correspond to actual fields of `contentcuration.models.Channel`
    channel_pk = indexes.FacetCharField()
    channel_name = indexes.CharField()
    channel_public = indexes.FacetBooleanField()
    channel_deleted = indexes.FacetBooleanField()

    @staticmethod
    def indexed_channel_fields():
        return [field[len('channel_'):] for field,_ in ContentNodeChannelInfo.fields.items()]

    def prepare_channel_info(self, obj):
        from contentcuration.models import ContentNode
        if isinstance(obj, ContentNode):
            obj = obj.get_channel()
        if not obj:
            return dict()
        return {
            ('channel_%s' % field): obj.__getattribute__(field)
            for field in self.indexed_channel_fields()
        }

class ContentNodeIndex(ContentNodeChannelInfo, CelerySearchIndex, indexes.Indexable, PartiallyUpdatableIndex):
    text = indexes.CharField(use_template=True, document=True)
    title = indexes.NgramField(model_attr='title')
    content_kind = indexes.CharField(model_attr='kind__kind', faceted=True)
    published = indexes.BooleanField(model_attr='published', faceted=True)
    language = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return ContentNode

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

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

    def prepare(self, obj):
        self.prepared_data = super(ContentNodeIndex, self).prepare(obj)
        self.prepared_data.update(self.prepare_channel_info(obj))
        return self.prepared_data

class ChannelIndex(CelerySearchIndex, indexes.Indexable, PartiallyUpdatableIndex):
    text = indexes.CharField(use_template=True, document=True)
    name = indexes.NgramField(model_attr='name')
    public = indexes.BooleanField(model_attr='public', faceted=True)
    language = indexes.MultiValueField(faceted=True)

    channel_editors = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Channel

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

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

    def prepare_channel_editors(self, channel):
        if channel:
            return [str(ed.id) for ed in channel.editors.all()]
        else:
            return []
