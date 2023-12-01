import logging
import os

import boto3

from models import S3Record

# Configure S3 client
s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "eu-west-2"))

# The output bucket name
PREPROCESSED_OUTPUT_BUCKET_NAME = os.environ.get("PREPROCESSED_OUTPUT_BUCKET_NAME")

# Configure logging
logger = logging.getLogger("data-preprocessing")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    s3_record = S3Record(event)
    logger.info(
        "Received event: %s on bucket: %s", s3_record.bucket_name, s3_record.bucket_name
    )
    return event
