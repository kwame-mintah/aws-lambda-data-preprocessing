import pytest

import data_preprocessing


@pytest.fixture(autouse=True)
def set_environment_name(monkeypatch):
    monkeypatch.setattr(data_preprocessing, "SERVERLESS_ENVIRONMENT", "local")
