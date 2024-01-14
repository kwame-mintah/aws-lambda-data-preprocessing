import io

import botocore.session
import pytest
from botocore.stub import Stubber, ANY

from data_preprocessing import (
    pre_checks_before_processing,
    retrieve_and_convert_to_dataframe,
    upload_to_output_bucket,
    mark_as_processed,
)
from exmaple_responses import (
    example_tag_set_without_processed_time,
    example_tag_set_with_processed_time,
    example_get_object,
    example_get_put_object,
)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("incorrect.md", example_tag_set_without_processed_time(), True),
        ("correct.csv", example_tag_set_without_processed_time(), None),
        ("correct.csv", example_tag_set_with_processed_time(), True),
    ],
)
def test_pre_checks_before_processing(a, b, expected):
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Bucket": ANY, "Key": ANY}
    stubber.add_response("get_object_tagging", b, expected_params)

    with stubber:
        result = pre_checks_before_processing(a, "ProcessedTime", s3_client)
        assert result is expected


def test_retrieve_and_convert_to_dataframe():
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Bucket": ANY, "Key": ANY}
    stubber.add_response("get_object", example_get_object(), expected_params)

    with stubber:
        result = retrieve_and_convert_to_dataframe("example-bank-file.csv", s3_client)
        assert result.shape[1] == 21


def test_upload_to_output_bucket():
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Body": ANY, "Bucket": ANY, "Key": ANY, "Tagging": ANY}
    stubber.add_response("put_object", example_get_put_object(), expected_params)
    file_obj = io.BytesIO()

    with stubber:
        result = upload_to_output_bucket(file_obj, "example-bank-file.csv", s3_client)
        assert result is None


def test_mark_as_processed():
    s3_client = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3_client)
    expected_params = {"Bucket": ANY, "Key": ANY, "Tagging": ANY}
    stubber.add_response("put_object_tagging", {}, expected_params)

    with stubber:
        result = mark_as_processed("example-bank-file.csv", s3_client)
        assert result is None
