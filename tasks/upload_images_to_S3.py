from os.path import basename, dirname, join, abspath
from glob import glob

from boto.s3 import connect_to_region
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key

# Gets credential from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
conn = connect_to_region(Location.APSoutheast2)

bucket = conn.get_bucket('bcaron')

IMAGE_DIR = join(dirname(dirname(abspath(__file__))), 'static', 'uploads')

all_keys = [k.key for k in bucket.list()]

print('all_keys', all_keys)

for image_filepath in glob(join(IMAGE_DIR, '*')):
    if basename(image_filepath) not in all_keys:
        print('Uploading image_filepath {0} to bucket'.format(image_filepath))
        k = Key(bucket)
        k.key = basename(image_filepath)
        k.set_contents_from_filename(image_filepath)
        k.set_acl('public-read')
    else:
        print('image_filepath {0} already in bucket'.format(image_filepath))
