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
        topic, _ = ContentKind.objects.get_or_create(kind="Topic")

        # original_title = ''.join(choice(ascii_letters) for l in range(20))
        node= ContentNode.objects.create(kind=topic)

        random_text = 'abc'
        self.assertEqual(
            len(SearchQuerySet().filter(some_field=random_text)),
            0
        )

        ContentNodeIndex().partial_update(node, some_field=random_text)

        self.assertEqual(
            len(SearchQuerySet().filter(some_field=random_text)),
            1
        )

        ContentNodeIndex().update_object(node)

        self.assertEqual(
            len(SearchQuerySet().filter(some_field=random_text)),
            1
        )



