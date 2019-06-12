from haystack.utils import get_identifier, get_model_ct
from haystack import indexes
from haystack_elasticsearch5 import Elasticsearch5SearchBackend, Elasticsearch5SearchEngine
from elasticsearch.helpers import bulk
from haystack.constants import ID

def partial_data(identifier, **fields):
    data = {
        '_op_type': 'update',
        '_id': identifier,
    }
    data['doc'] = fields
    return data

class StudioElasticsearchBackend(Elasticsearch5SearchBackend):

    def partial_update(self, data):
        print(data)
        bulk(self.conn, data, index=self.index_name, doc_type='modelresult')
        self.conn.indices.refresh(index=self.index_name)

class StudioElasticsearchEngine(Elasticsearch5SearchEngine):
    backend = StudioElasticsearchBackend


class PartiallyUpdatableIndex(object):
    # Given a queryset, update one or more objects search index document without
    # touching the main DB.
    #
    # Note: index updates performed this way will be overwritten when haystack
    # reindexes their corresponding objects.
    def partial_update(self, queryset_or_obj, **fields):
        try:
            pks = queryset_or_obj.values_list('pk', flat=True)
        except AttributeError:
            pks = [queryset_or_obj.pk]
        identifiers = (
            "%s.%s" % (get_model_ct(self.get_model()), pk)
            for pk in pks
        )

        data = [partial_data(id, **fields) for id in identifiers]
        self.get_backend().partial_update(data)
