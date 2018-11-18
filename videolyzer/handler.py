import urllib
import boto3

def start_processing_video(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        start_label_detection(bucket_name, key)

    return event


def start_label_detection(bucket_name, key):
    rekcognition = boto3.client('rekcognition')
    response = rekcognition.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': key
            }
        }
    )

    print(response)

    return