"""Lambda function to process completed Rekognition jobs"""

import json
import os
from decimal import Decimal

import boto3


def handler(event, context):
    """Handles SNS message on Rekognition job completion"""
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        job_id = message['JobId']
        key = message['Video']['S3ObjectName']
        bucket = message['Video']['S3Bucket']

        response = get_video_labels(job_id)
        print(response)
        put_labels_in_db(response, key, bucket)

    return event


def get_video_labels(job_id):
    """Fetches video labels from Rekognition"""
    rekognition = boto3.client('rekognition')

    response = rekognition.get_label_detection(JobId=job_id)
    next_token = response.get('NextToken', None)

    while next_token:
        next_response = rekognition.get_label_detection(
            JobId=job_id,
            NextToken=next_token
        )
        next_token = next_response.get('NextToken', None)

        response['Labels'].extend(next_response['Labels'])

    return response


def put_labels_in_db(data, key, bucket):
    """Puts label data into DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    videos_table = dynamodb.Table(table_name)

    del data['ResponseMetadata']
    del data['JobStatus']

    data['videoName'] = key
    data['videoBucket'] = bucket

    data = make_item(data)

    videos_table.put_item(Item=data)


def make_item(data):
    """Convert floats to Decimal for DynamoDB"""
    if isinstance(data, dict):
        return {k: make_item(v) for k, v in data.items()}

    if isinstance(data, list):
        return [make_item(v) for v in data]

    if isinstance(data, float):
        return Decimal(str(data))

    return data
