import os

import pytest
from fastapi.testclient import TestClient

from network_coverage_api.app.main import app


@pytest.fixture(scope="function")
def testclient():

    with TestClient(app) as client:
        yield client
