from django.test import TestCase  # noqa
from django.utils import timezone
from .models import Print, Tag
import datetime

#  Create your tests here.

class SimplexMethodtests(TestCase):
    
    def test_db_insert(self ):
        """
        """
        time = timezone.now()
        testTag = Tag("test",1.0)
        print_in_es = Print(title="test",description="test", file_path="test",image_file="test",
                            thumbnail_file="test",print_file="test",price="test",tags=testTag
                            , created_at=timezone.now(),modified_at=timezone.now())
        #self.assertEqual(len(Print.objects.search.query('title', _all='test')), 1)