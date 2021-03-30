from os import walk
from os.path import basename, dirname, join, abspath, exists
from glob import glob
from argparse import ArgumentParser, Namespace

from boto3 import client

from application import APPLICATION

BUCKET_NAME = 'cv.bcaron.me'

# Should match the one in your S3 bucket config
INDEX_FILENAME = 'cv.html'

ROUTES = ['cv', 'contact']

IMAGE_DIR = join(dirname(dirname(abspath(__file__))), 'static', 'uploads')

IMAGE_EXTENSIONS = {'.jpg', '.png', '.jpeg', '.pdf'}

S3_CLIENT = client('s3')#, region="ap-southeast-2")

def upload(bucket: str) -> None:
    def upload_static_page(page_name: str) -> None:
        client = APPLICATION.test_client()
        response = client.get('/{page_name}'.format(page_name=page_name))

        page_filename = '{page_name}.html'.format(page_name=page_name) if page_name == INDEX_FILENAME.split('.')[0] else page_name

        with open(page_filename, 'wb') as fh:
            fh.write(response.get_data())

        print('Uploading {0} to ${1}'.format(page_filename, page_filename))
        S3_CLIENT.upload_file(page_filename, bucket, page_filename, ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/html; charset=utf-8'})

    [
        upload_static_page(route)
        for route in ROUTES
    ]

    # Upload all static assets
    for (root, subdirs, files) in walk('static'):
        for _file in files:
            filename = join(root, _file)
            S3_CLIENT.upload_file(filename, bucket, filename, ExtraArgs={'ACL': 'public-read'})

def download(bucket: str) -> None:
    for k in bucket.list():
        if any(k.key.endswith(extension) for extension in IMAGE_EXTENSIONS):
            image_filepath = join(IMAGE_DIR, k.key)
            if not exists(image_filepath):
                print('Will download {0}'.format(k.key))
                k.get_contents_to_filename(image_filepath)
            else:
                print('No need to download {0}'.format(k.key))
        else:
            print('No an image: {0}'.format(k.key))

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--upload', action='store_true')
    parser.add_argument('--download', action='store_true')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    # Gets credential from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    response = S3_CLIENT.list_objects_v2(Bucket=BUCKET_NAME) # TODO: Handle continuation here

    print('all_keys', [k['Key'] for k in response['Contents']])

    if args.upload:
        upload(BUCKET_NAME)

    if args.download:
        download(BUCKET_NAME)
