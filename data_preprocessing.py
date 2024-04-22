import io
import logging
import os  # For manipulating filepath names
from datetime import datetime
from typing import Any

import boto3
import pandas as pd  # For munging tabular data
from pandas import DataFrame

from models import S3Record

# The AWS region
aws_region = os.environ.get("AWS_REGION", "eu-west-2")

# Configure S3 client
s3_client = boto3.client("s3", region_name=aws_region)

# The environment the lambda is currently deployed in
SERVERLESS_ENVIRONMENT = os.environ.get("SERVERLESS_ENVIRONMENT")

# Configure logging
logger = logging.getLogger("data-preprocessing")
logger.setLevel(logging.INFO)

# Output file dir
preprocess_file_dir = "automl/{}/".format(str(datetime.now().strftime("%Y-%m-%d")))

# The output bucket ssm parameter store name
ssm_preprocessed_output_bucket_name = "mlops-eu-west-2-{}-automl-data".format(
    SERVERLESS_ENVIRONMENT
)


def lambda_handler(event, context):
    """
    Perform data preprocessing on new data received

    :param event: AWS S3 Event received
    :param context:
    :return: event
    """
    s3_record = S3Record(event)
    logger.info(
        "Received event: %s on bucket: %s for object: %s",
        s3_record.event_name,
        s3_record.bucket_name,
        s3_record.object,
    )

    if pre_checks_before_processing(
        bucket_name=s3_record.bucket_name,
        key=s3_record.object,
        find_tag="ProcessedTime",
    ):
        return

    # Load the data recently uploaded to the bucket
    data = retrieve_and_convert_to_dataframe(
        bucket_name=s3_record.bucket_name, key=s3_record.object
    )
    # Replace values within the dataframe
    data.replace(r"\.", "_", regex=True)
    dataframe = data.replace(r"\_$", "", regex=True)
    # Add two new indicators
    dataframe["no_previous_contact"] = (dataframe["pdays"] == 999).astype(int)
    dataframe["not_working"] = (
        dataframe["job"].isin(["student", "retired", "unemployed"]).astype(int)
    )
    # TODO: Convert categorical variables to sets of indicators

    # Drop irrelevant features
    dataframe = dataframe.drop(
        [
            "duration",
            "emp.var.rate",
            "cons.price.idx",
            "cons.conf.idx",
            "euribor3m",
            "nr.employed",
        ],
        axis=1,
    )
    logger.info("Finished converting columns / removing features from data.")
    file_obj = io.BytesIO()
    dataframe.to_csv(file_obj, lineterminator="\n", index=False)
    file_obj.seek(0)

    # Upload csv to output bucket for training
    preprocessed_output_bucket_name = get_parameter_store_value(
        name=ssm_preprocessed_output_bucket_name
    )
    upload_to_output_bucket(
        bucket_name=preprocessed_output_bucket_name,
        file_obj=file_obj,
        key=preprocess_file_dir + s3_record.object,
    )
    mark_as_processed(bucket_name=s3_record.bucket_name, key=s3_record.object)
    logger.info(
        "Data preprocessing complete and uploaded to %s bucket.",
        preprocessed_output_bucket_name,
    )
    return event


def pre_checks_before_processing(
    bucket_name: str, key: str, find_tag: str, client: Any = s3_client
) -> bool:
    """
    Check that the object is a csv file and has not been processed previously.

    :param bucket_name: The bucket name containing the object.
    :param key: The full path for to object
    :param find_tag: Tag to find on the object
    :param client: boto3 client configured to use s3
    :return: bool
    """
    object_tags = client.get_object_tagging(Bucket=bucket_name, Key=key)
    if ".csv" not in key:
        logger.info("Will not process, expected object to be a csv.")
        return True
    else:
        for tag in object_tags["TagSet"]:
            if find_tag in tag:
                logger.info("Object has previously been processed.")
                return True
    return False


def retrieve_and_convert_to_dataframe(
    bucket_name: str, key: str, client: Any = s3_client
) -> DataFrame:
    """
    Get the csv file from the bucket and return as a DataFrame.

    :param bucket_name: The bucket name containing the object.
    :param key: The full path for to object
    :param client: boto3 client configured to use s3
    :return: DataFrame
    """
    s3_object = client.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(s3_object["Body"])


def upload_to_output_bucket(
    bucket_name: str, file_obj: io.BytesIO, key: str, client: Any = s3_client
) -> None:
    """
    Upload the file object to the output s3 bucket.

    :param bucket_name: The bucket name to upload the object.
    :param file_obj: The DataFrame as a csv
    :param key: The full path to the object destination
    :param client: boto3 client configured to use s3
    :return:
    """
    client.put_object(
        Body=file_obj,
        Bucket=bucket_name,
        Tagging="ProcessedTime=%s" % str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        Key=key,
    )


def mark_as_processed(bucket_name: str, key: str, client: Any = s3_client) -> None:
    """
    Add a tag to the csv that has now been processed.

    :param bucket_name: The bucket name containing the object.
    :param key: Key of the object to get.
    :param client: boto3 client configured to use s3
    :return:
    """
    client.put_object_tagging(
        Bucket=bucket_name,
        Tagging={
            "TagSet": [
                {
                    "Key": "ProcessedTime",
                    "Value": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                },
            ]
        },
        Key=key,
    )


def get_parameter_store_value(
    name: str, client: Any = boto3.client("ssm", region_name=aws_region)
) -> str:
    """
    Get a parameter store value from AWS.

    :param name: The name or Amazon Resource Name (ARN) of the parameter that you want to query
    :param client: boto3 client configured to use ssm
    :return: value
    """
    logger.info("Retrieving %s from parameter store", name)
    return client.get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]
