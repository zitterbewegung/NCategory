from .models import Print
from bungiesearch.fields import DateField, StringField
from bungiesearch.indices import ModelIndex


class PrintIndex(ModelIndex):
    effectived_date = DateField(eval_as='obj.created_at if obj.created_at and obj.modified_at > obj.created_at else obj.modified_at')
    meta_data = StringField(eval_as='" ".join([fld for fld in [str(obj.created_at), str(obj.tags), str(obj.price)] if fld])')

    class Meta:
        model = Print
        exclude = ('file_path', 'thumbnail_file' )
        hotfixes = {'title': {'boost': 1.75},
                    'description': {'boost': 1.35},
                    'tags': {'boost': 2.0}}
