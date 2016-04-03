from django.test import TestCase  # noqa
from django.utils import timezone
from .models import Print, Tag

#  Create your tests here.


class SimplexMethodtests(TestCase):

    def test_db_insert(self):
        """
        Test for database entry creation
        """

        testTag = Tag("test", 1.0)
        print_in_es = Print(title="test", description="test", file_path="test", image_file="test",
                            thumbnail_file="test", print_file="test", price="test", tags=testTag,
                            created_at=timezone.now(), modified_at=timezone.now())
        self.assertEqual(print_in_es.title, "test")
        # self.assertEqual(len(Print.objects.search.query('title', _all='test')), 1)
