from django.test import TestCase  # noqa
from django.utils import timezone
from .models import Print, Tag
import tempfile, subprocess
from .tasks import generate_tags
from .utility import convert_ply_pcd, pcd_to_vfh_histogram
from django.conf import settings
from .celeryconf import app
#  Create your tests here.


class TestFeatureExtraction(TestCase):
    cube_obj= """
    v  1 -1 -1
    v -1 -1 -1
    v  1  1  1
    v -1 -1  1
    v  1 -1  1
    v -1  1  1
    v  1  1 -1
    v -1  1 -1
    f 7 1 2
    f 7 2 8
    f 3 6 4
    f 3 4 5
    f 7 3 5
    f 7 5 1
    f 1 5 4
    f 1 4 2
    f 2 4 6
    f 2 6 8
    f 3 7 8
    f 3 8 6

    """
    cube_ascii_pcd = """# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH 8
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS 8
DATA ascii
1 -1 -1
-1 -1 -1
1 1 1
-1 -1 1
1 -1 1
-1 1 1
1 1 -1
-1 1 -1
"""

    cube_vfh_feature = """# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS vfh
SIZE 4
TYPE F
COUNT 308
WIDTH 1
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS 1
DATA ascii
114.28571 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 114.28571 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 114.28571 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 100 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
"""
    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True
        app.conf.CELERY_ALWAYS_EAGER = True

    def create_pcd_file():
        """
        
        """
        pass  
        
    def test_convert_ply_pcd(self):
        """
        tests that using the subprocess ply2pcd program works.
        """
        with tempfile.NamedTemporaryFile(suffix='.obj') as fp:
            fp.write(self.cube_obj.encode('UTF-8'))
            fp.flush()
            convert_ply_pcd(fp.name, '/tmp/cube.pcd')
        
            
        with open('/tmp/cube.pcd', mode='r', encoding="UTF-8") as fout, tempfile.TemporaryFile(mode='r+', encoding="UTF-8") as result_file:
            processed_string = fout.read()
            result_file.write(self.cube_ascii_pcd)
            result_file.flush()
            result_file.seek(0)
            result_string = result_file.read()
            self.assertMultiLineEqual(result_string, processed_string)

    def test_vfh_feature(self):
                
        with tempfile.NamedTemporaryFile(suffix='.pcd', encoding="UTF-8", mode='r+') as fp,  tempfile.NamedTemporaryFile(suffix='.pcd',mode='r+', encoding="UTF-8") as test_file,  tempfile.NamedTemporaryFile(suffix='.pcd', mode='r+', encoding="UTF-8") as result_file:
            fp.write(self.cube_vfh_feature)
            fp.flush()
            test_file.write(self.cube_ascii_pcd)
            test_file.flush()
            pcd_to_vfh_histogram(test_file.name, result_file.name)
            fp.seek(0)
            test_file.seek(0)
            processed_string = fp.read()
            result_string = result_file.read()
            self.assertMultiLineEqual(result_string, processed_string)
                
                
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
