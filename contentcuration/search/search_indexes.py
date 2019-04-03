from haystack import indexes
from contentcuration.models import ContentNode


class ContentNodeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='description', document=True)

    def get_model(self):
        return ContentNode

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(published=True)
