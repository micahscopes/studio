from haystack_elasticsearch5 import *
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
