from django.test import TestCase
from django.test import TransactionTestCase
from contentcuration.tests.testdata import topic
from .search_indexes import ContentNodeIndex
from haystack.query import SearchQuerySet
from random import choice
from string import ascii_letters
from contentcuration.models import ContentNode, ContentKind

class TestPartialUpdate(TransactionTestCase):
    def test_partial_update_contentnode(self):
        import ipdb; ipdb.set_trace()
        topic, _ = ContentKind.objects.get_or_create(kind="Topic")
        node= ContentNode.objects.create(title='Some Topic', kind=topic)
        titleA = ''.join(choice(ascii_letters) for l in range(23))
        titleB = ''.join(choice(ascii_letters) for l in range(23))

        node.title=titleA
        ContentNodeIndex().partial_update(node, title=titleA)

        import ipdb; ipdb.set_trace()



