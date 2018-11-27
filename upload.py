from pathlib import Path

import click
import boto3
from botocore.exceptions import ClientError

@click.command()
@click.argument('bucket_name')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--profile', default=None, help='Specify the AWS profile to use as credentials.')
def upload(bucket_name=None, file_path=None, **kwargs):
    """Upload to <BUCKET_NAME> <FILE_PATH>"""
    params = {k:v for k, v in kwargs.items() if v is not None}
    session = boto3.Session(**params)
    s3 = session.resource('s3')

    try:
        bucket = s3.Bucket(bucket_name)
        path = Path(file_path).expanduser().resolve()
        bucket.upload_file(str(path), str(path.name))

    except ClientError as err:
        print('Unable to upload file {0}. '.format(file_path) + str(err) + '\n')

    return


if __name__ == '__main__':
    upload()