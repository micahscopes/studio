from haystack import indexes
from contentcuration.models import ContentNode, Channel
from celery_haystack.indexes import CelerySearchIndex
from haystack.utils import get_identifier, get_model_ct
from .utils import partial_doc

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

    def partial_update(self, contentnode, **fields):
        docs = [partial_doc(get_identifier(contentnode), **fields)]
        self.get_backend().partial_update(docs)

    def partial_update_tree(self, parent, **fields):
        child_identifiers = (
            "%s.%s" % (get_model_ct(contentnode), pk)
            for pk in oarent.children.all().values_list('pk', flat=True)
        )

        parent_doc = [partial_doc(get_identifier(contentnode), **fields)]
        child_docs = [partial_doc(identifier, **fields) for identifier in child_identifiers]
        self.get_backend().partial_update(parent_doc+child_docs)



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


