import urllib
import os

import boto3

def handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        start_label_detection(bucket_name, key)

    return event


def start_label_detection(bucket_name, key):
    rekognition = boto3.client('rekognition')
    response = rekognition.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': key
            }
        },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
        }
    )

    print(response)

    return