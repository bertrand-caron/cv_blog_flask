from os import walk
from os.path import basename, dirname, join, abspath, exists
from glob import glob
from argparse import ArgumentParser, Namespace
from itertools import chain

from boto3 import client

from application import APPLICATION

BUCKET_NAME = 'cv.bcaron.me'

# Should match the one in your S3 bucket config
INDEX_FILENAME = 'cv.html'

ROUTES = ['cv', 'contact']

IMAGE_DIR = join(dirname(dirname(abspath(__file__))), 'static', 'uploads')

IMAGE_EXTENSIONS = {'.jpg', '.png', '.jpeg', '.pdf'}

S3_CLIENT = client('s3')#, region="ap-southeast-2")

def upload(bucket: str, dry_run: bool = False) -> None:
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

    exit()
    # Upload all static assets (with public-read)
    for (root, subdirs, files) in walk('static'):
        for _file in files:
            filename = join(root, _file)

            # Exclude the .gitignore file
            if _file == '.gitignore': continue

            if not dry_run:
                print('Uploading {0} to {1}'.format(filename, bucket))
                S3_CLIENT.upload_file(filename, bucket, filename, ExtraArgs={'ACL': 'public-read'})

    # Upload data and config (without public-read)
    for (root, subdirs, files) in chain(walk('data'), walk('config')):
        for _file in files:
            filename = join(root, _file)

            # Do not upload example files
            if _file.endswith('.example'): continue
            # Do not upload git folders
            if '/.git/' in filename: continue

            print('Uploading {0} to {1}'.format(filename, bucket))
            if not dry_run:
                S3_CLIENT.upload_file(filename, bucket, filename)

def download(bucket: str, dry_run: bool = False) -> None:
    for k in S3_CLIENT.list_objects_v2(Bucket=BUCKET_NAME)['Contents']:
        filepath = k['Key']
        if not exists(filepath):
            print('Will download {0}'.format(filepath))
            if not dry_run:
                S3_CLIENT.download_file(BUCKET_NAME, k['Key'], filepath)
        else:
            print('No need to download {0} (already exists, will not overwrite)'.format(k['Key']))

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('--upload', action='store_true')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--dry-run', action='store_true')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    # Gets credential from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    response = S3_CLIENT.list_objects_v2(Bucket=BUCKET_NAME) # TODO: Handle continuation here

    print('all_keys', [k['Key'] for k in response['Contents']])

    if args.upload:
        upload(BUCKET_NAME, dry_run=args.dry_run)

    if args.download:
        download(BUCKET_NAME, dry_run=args.dry_run)
