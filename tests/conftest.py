import pytest

import data_preprocessing


@pytest.fixture(autouse=True)
def set_bucket_name(monkeypatch):
    monkeypatch.setattr(
        data_preprocessing, "PREPROCESSED_OUTPUT_BUCKET_NAME", "unit-test"
    )
