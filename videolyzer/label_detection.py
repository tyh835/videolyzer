import json
import boto3


def handler(event, context):
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
    return