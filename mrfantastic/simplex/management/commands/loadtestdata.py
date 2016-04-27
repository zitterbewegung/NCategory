from mrfantastic.simplex.models import Print, Tag, Account
from django.core.management.base import BaseCommand
from django.utils import timezone
from mrfantastic.simplex.utility import pcd_to_vfh_histogram, convert_obj_pcd

class Command(BaseCommand):

    help = "Whatever you want to print here"

    def handle(self, *args, **options):
        data_dir = '/app/data/GroundTruthDatabase/'
        serving_path = "/static/GroundTruthDatabase/"
        with open(data_dir + 'all_1833.txt', 'r') as infile:
            for line in infile:
                thumbnail = serving_path + line.strip().replace("\\", "/") + ".jpg"
                objfile = serving_path + line.strip().replace("\\", "/") + ".obj"
                datafile = data_dir + line.strip().replace("\\", "/") + ".obj"
                tag_text = line.split("\\")[0].replace("1_", "")
                testTag = Tag(category=str(tag_text), confidence=1.0)
                test_account = Account.objects.all()[0] 
                convert_obj_pcd(datafile, datafile + '.pcd')
                #import pdb; pdb.set_trace()
                pcd_to_vfh_histogram(datafile + '.pcd', datafile + '_vfh' + '.pcd')
                print_obj = Print(title=line, description="Ground truth database",
                                  file_path=objfile, image_file=thumbnail,
                                  thumbnail_file=thumbnail, print_file=objfile,
                                  price=float("9.99"), tags=testTag, author=test_account,
                                  created_at=timezone.now(), modified_at=timezone.now())
                testTag.save()
                print_obj.save()
