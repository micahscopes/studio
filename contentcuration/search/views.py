from django.db.models import Q
from contentcuration import models as cc_models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from contentcuration import serializers


def get_accessible_contentnodes(request):
    exclude_channel = request.query_params.get('exclude_channel', '')

    # Get tree_ids for channels accessible to the user
    tree_ids = cc_models.Channel.objects \
        .select_related('main_tree') \
        .filter(Q(deleted=False) & (Q(public=True) | Q(editors=request.user) | Q(viewers=request.user))) \

    if exclude_channel is not None:
        tree_ids = tree_ids.exclude(pk=exclude_channel)

    tree_ids = tree_ids.values_list('main_tree__tree_id', flat=True)

    return cc_models.ContentNode.objects \
        .filter(tree_id__in=tree_ids)

from rest_framework.pagination import PageNumberPagination
class Paginator(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000

@api_view(['GET'])
def search_items(request):
    """
    Keyword search of items (i.e. non-topics)
    """
    search_query = request.query_params.get('q', '').strip()

    if search_query == '':
        # TODO maybe return a proper error code
        return Response([])

    queryset = get_accessible_contentnodes(request).exclude(kind='topic')
    queryset = queryset.filter(title__icontains=search_query)
    queryset = Paginator().paginate_queryset(queryset, request)
    # Using same serializer as Tree View UI to match props of ImportListItem
    serializer = serializers.SimplifiedContentNodeSerializer(queryset[:50], many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_topics(request):
    """
    Keyword search of topics
    """
    search_query = request.query_params.get('q', '').strip()

    if search_query == '':
        return Response([])

    queryset = get_accessible_contentnodes(request).filter(kind='topic')
    queryset = queryset.filter(title__icontains=search_query)
    queryset = Paginator().paginate_queryset(queryset, request)
    serializer = serializers.SimplifiedContentNodeSerializer(queryset[:50], many=True)
    return Response(serializer.data)

from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet


from .search_indexes import ContentNode
from .search_indexes import ContentNodeIndex
from contentcuration.serializers import ContentNodeSerializer


class ContentNodeResultSerializer(HaystackSerializer):
    serialize_objects = True
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [ContentNodeIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes. These
        # fields belong to the search index!
        fields = [
            "title", "language", "content_kind", "channel_id", "pk"
        ]


class ContentNodeSearchView(HaystackViewSet):

    # `index_models` is an optional list of which models you would like to include
    # in the search result. You might have several models indexed, and this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the scenes.
    index_models = [ContentNode]

    serializer_class = ContentNodeResultSerializer
