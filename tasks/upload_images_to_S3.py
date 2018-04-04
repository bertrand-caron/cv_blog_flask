from os.path import basename, dirname, join, abspath, exists
from glob import glob
from argparse import ArgumentParser, Namespace

from boto.s3 import connect_to_region
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key
from boto.s3.bucket import Bucket

IMAGE_DIR = join(dirname(dirname(abspath(__file__))), 'static', 'uploads')

IMAGE_EXTENSIONS = {'.jpg', '.png', '.jpeg', '.pdf'}

def upload(bucket: Bucket) -> None:
    for image_filepath in glob(join(IMAGE_DIR, '*')):
        if basename(image_filepath) not in all_keys:
            print('Uploading image_filepath {0} to bucket'.format(image_filepath))
            k = Key(bucket)
            k.key = basename(image_filepath)
            k.set_contents_from_filename(image_filepath)
            k.set_acl('public-read')
        else:
            print('image_filepath {0} already in bucket'.format(image_filepath))

def download(bucket: Bucket) -> None:
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
    conn = connect_to_region(Location.APSoutheast2)
    bucket = conn.get_bucket('bcaron')
    all_keys = [k.key for k in bucket.list()]

    print('all_keys', all_keys)

    if args.upload:
        upload(bucket)

    if args.download:
        download(bucket)
