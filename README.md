# Videolyzer

Video (mp4) analysis using AWS Rekognition and Lambda (python3.6) built on the Serverless Framework.

Before deployment, make sure to create a configuration file using `config.template.json` and enter the relevant details. For `stage: dev`, the config file should be named `config.dev.json`, etc.

## Uploading Videos

Included is a Python script for uploading videos. To use, run `pipenv install` and `pipenv run python upload.py <BUCKET_NAME> <FILE_PATH>` to upload to target S3 bucket.