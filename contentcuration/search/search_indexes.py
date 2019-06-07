from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from haystack.utils import get_identifier, get_model_ct
from .utils import partial_data

import fields

class PartialUpdateMixin(object):
    # Given a queryset, update one or more objects search index document without
    # touching the main DB.
    #
    # Note: index updates performed this way will be overwritten when haystack
    # reindexes their corresponding objects.
    def partial_update(self, queryset, **fields):
        identifiers = (
            "%s.%s" % (get_model_ct(self.get_model()), pk)
            for pk in queryset.values_list('pk', flat=True)
        )

        data = [partial_data(id, **fields) for id in identifiers]
        self.get_backend().partial_update(data)

class ContentNodeIndex(CelerySearchIndex, indexes.Indexable, PartialUpdateMixin):
    text = indexes.CharField(use_template=True, document=True)
    title = indexes.NgramField(model_attr='title')
    channel_id = fields.ChannelIdField(model_attr='get_channel', faceted=True)
    channel_info = indexes.MultiValueField(faceted=True)
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

    # def partial_update_tree(self, parent, **fields):
    #     return self.partial_update(parent.children.all(), **fields)

    def prepare_channel_info(self, contentnode):
        return ContentNodeIndex.get_channel_info(contentnode)

    indexed_channel_fields = [
        "pk",
        "title",
    ]

    @staticmethod
    def get_channel_info(obj):
        if isinstance(object, ContentNode):
            ContentNodeIndex.get_channel_index_info(obj.get_channel())
        elif isinstance(object, Channel):
            fields = ContentNodeIndex.indexed_channel_fields
            return object.values_list(*fields, flat=True)

class ChannelIndex(CelerySearchIndex, indexes.Indexable, PartialUpdateMixin):
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
