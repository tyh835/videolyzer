from pathlib import Path

import click
import boto3
from botocore.exceptions import ClientError

@click.argument('path_name', type=click.Path(exists=True))
@click.argument('bucket_name')
@click.option('--profile', default=None, help='Specify the AWS profile to use as credentials.')
def hello(path_name, bucket_name, **kwargs):
    """Upload <PATH> to <BUCKET_NAME>"""
    params = {k:v for k, v in kwargs.items() if v is not None}
    session = boto3.Session(**params)
    s3 = session.resource('s3')

    try:
        bucket = s3.Bucket(bucket_name)
        path = Path(path_name).expanduser().resolve()
        bucket.upload_file(str(path), str(path.name))

    except ClientError as err:
        print('Unable to upload file {0}. '.format(path_name) + str(err) + '\n')

    return