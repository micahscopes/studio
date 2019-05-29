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
        # import ipdb; ipdb.set_trace()
        topic, _ = ContentKind.objects.get_or_create(kind="Topic")
        original_title = ''.join(choice(ascii_letters) for l in range(20))
        node= ContentNode.objects.create(title=original_title, kind=topic)
        self.assertEqual(
            len(SearchQuerySet().filter(title=original_title)),
            1
        )

        new_title = ''.join(choice(ascii_letters) for l in range(20))
        ContentNodeIndex().partial_update(node, title=new_title)

        self.assertEqual(
            len(SearchQuerySet().filter(title=original_title)),
            0
        )

        self.assertEqual(
            len(SearchQuerySet().filter(title=new_title)),
            1
        )



