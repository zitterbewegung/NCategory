import boto
import mimetypes
import json

conn = boto.connect_s3('AWS_KEY', 'AWS_SECRET')

def sign_s3_upload(request):
    object_name = request.GET['objectName']
    content_type = mimetypes.guess_type(object_name)[0]

    signed_url = conn.generate_url(
        300,
        "PUT",
        'BUCKET_NAME',
        'FOLDER_NAME' + object_name,
        headers = {'Content-Type': content_type, 'x-amz-acl':'public-read'})

        return HttpResponse(json.dumps({'signedUrl': signed_url}))