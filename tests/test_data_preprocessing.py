import io
from pathlib import Path

import botocore.session
import pandas as pd
import pytest
from botocore.stub import Stubber, ANY

import data_preprocessing
from data_preprocessing import (
    pre_checks_before_processing,
    retrieve_and_convert_to_dataframe,
    upload_to_output_bucket,
    mark_as_processed,
    lambda_handler,
    get_parameter_store_value,
)
from example_responses import (
    example_tag_set_without_processed_time,
    example_tag_set_with_processed_time,
    example_get_object,
    example_get_put_object,
    example_event,
    example_empty_tag_set,
    example_parameters_response,
)

LOCAL_TEST_FILENAME = str(Path(__file__).parent / "example-bank-file.csv")


def test_lambda_handler(monkeypatch):

    def ssm_output_bucket(name):
        """
        Stub parameter store retrieval
        """
        return "value"

    def checks_passed(bucket_name, key, find_tag):
        """
        Stub checks on event
        """
        return False

    def return_dataframe(bucket_name, key):
        """
        Stub return local file
        """
        return pd.read_csv(LOCAL_TEST_FILENAME)

    def uploaded_to_bucket(bucket_name, file_obj, key):
        """
        Stub uploading to bucket
        """
        return None

    def tag_applied_to_object(bucket_name, key):
        """
        Stub adding tag to object
        """
        return None

    monkeypatch.setattr(
        data_preprocessing, "pre_checks_before_processing", checks_passed
    )
    monkeypatch.setattr(
        data_preprocessing, "get_parameter_store_value", ssm_output_bucket
    )
    monkeypatch.setattr(
        data_preprocessing, "retrieve_and_convert_to_dataframe", return_dataframe
    )
    monkeypatch.setattr(
        data_preprocessing, "upload_to_output_bucket", uploaded_to_bucket
    )
    monkeypatch.setattr(data_preprocessing, "mark_as_processed", tag_applied_to_object)

    result = lambda_handler(example_event(), None)
    assert result["Records"][0]["s3"]["object"]["key"] == "example-bank-file.csv"


@pytest.mark.parametrize(
    "key, aws_response, expected",
    [
        ("incorrect.md", example_tag_set_without_processed_time(), True),
        ("correct.csv", example_tag_set_without_processed_time(), False),
        ("correct.csv", example_empty_tag_set(), False),
        ("correct.csv", example_tag_set_with_processed_time(), False),
    ],
)
def test_pre_checks_before_processing(key, aws_response, expected):
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Bucket": ANY, "Key": ANY}
    stubber.add_response("get_object_tagging", aws_response, expected_params)

    with stubber:
        result = pre_checks_before_processing(
            "bucket-name", key, "ProcessedTime", s3_client
        )
        assert result is expected


def test_retrieve_and_convert_to_dataframe():
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Bucket": ANY, "Key": ANY}
    stubber.add_response("get_object", example_get_object(), expected_params)

    with stubber:
        result = retrieve_and_convert_to_dataframe(
            "bucket-name", LOCAL_TEST_FILENAME, s3_client
        )
        assert result.shape[1] == 21


def test_upload_to_output_bucket():
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Body": ANY, "Bucket": ANY, "Key": ANY, "Tagging": ANY}
    stubber.add_response("put_object", example_get_put_object(), expected_params)
    file_obj = io.BytesIO()

    with stubber:
        assert (
            upload_to_output_bucket(
                "bucket-name", file_obj, LOCAL_TEST_FILENAME, s3_client
            )
            is None
        )


def test_mark_as_processed():
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Bucket": ANY, "Key": ANY, "Tagging": ANY}
    stubber.add_response("put_object_tagging", {}, expected_params)

    with stubber:
        assert mark_as_processed("bucket-name", LOCAL_TEST_FILENAME, s3_client) is None


def test_get_parameter_store_value():
    ssm_client = botocore.session.get_session().create_client("ssm")
    stubber = Stubber(ssm_client)
    expected_params = {"Name": ANY, "WithDecryption": True}
    stubber.add_response(
        "get_parameter", example_parameters_response(), expected_params
    )

    with stubber:
        assert get_parameter_store_value("unit-test", ssm_client) == "string"
