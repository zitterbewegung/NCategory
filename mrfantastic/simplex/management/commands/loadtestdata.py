from mrfantastic.simplex.models import Print, Tag
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):

    help = "Whatever you want to print here"

    
    def handle(self,*args, **options):
        data_dir = '/app/data/GroundTruthDatabase/'
        with open(data_dir + 'all_1833.txt', 'r') as infile:
            for line in infile:
                thumbnail = data_dir + line.strip().replace("\\","/") + ".jpg"
                objfile = data_dir + line.strip().replace("\\","/") + ".obj"
                tag_text = line.split("\\")[0].replace("1_","")
                testTag = Tag(category=str(tag_text),confidence=1.0)
                print_obj =  Print(title=line,description="Test data, Ground truth database", file_path=objfile,image_file=thumbnail, thumbnail_file=thumbnail,print_file=objfile,price=float("9.99"),tags=testTag, created_at=timezone.now(),modified_at=timezone.now())
                testTag.save()
                print_obj.save()