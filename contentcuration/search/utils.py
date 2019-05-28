from haystack_elasticsearch5 import *
from elasticsearch.helpers import bulk
from haystack.constants import ID

def partial_doc(identifier, **fields):
    doc = {
        ID: identifier
    }
    doc.update(fields)
    return doc

class StudioElasticsearchBackend(Elasticsearch5SearchBackend):

    def partial_update(self, docs):
        bulk(self.conn, docs, index=self.index_name, doc_type='modelresult')
        self.conn.indices.refresh(index=self.index_name)

class StudioElasticsearchEngine(Elasticsearch5SearchEngine):
    backend = StudioElasticsearchBackend
