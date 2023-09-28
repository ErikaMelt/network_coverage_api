import json
from http import HTTPStatus

import pandas as pd
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from network_coverage_api.app.data_processing import (
    fetch_coordinates,
    find_network_coverage_data)
from network_coverage_api.app.main import app
from network_coverage_api.models.api_addrese_response import ApiAdresseResponse

client = TestClient(app)


@pytest.fixture()
def network_coverage_response():
    """Fixture that returns the address api data."""
    with open(
        "tests/resources/network_coverage_response.json", "r"
    ) as expected_response_json:
        return json.load(expected_response_json)


paris_addresses = [
    "42 rue papernest 75011 Paris",
    "138 Avenue de Paris 94300 Val-de-Marne",
    "Centre de Recherche des Cordeliers, 15 Rue de l'École de Médecine 75006 Paris",
]


@pytest.mark.parametrize("address", paris_addresses)
def test_get_network_coverage_200(network_coverage_response, address):
    with client as test_client:
        response = test_client.get(f"/network-coverage/?address={address}")
    assert response.status_code == 200
    assert response.json() == network_coverage_response[address]


def test_get_network_coverage_404():
    address = "xdljfdl"
    with client as test_client:
        response = test_client.get(f"/network-coverage/?address={address}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"


test_cases = [
    ("42 rue papernest 75011 Paris", 48.860248, 2.380383, 0.55276),
    ("42 elm street", None, None, None),  # Invalid address
    ("Equator Address", None, None, None),  # Coordinates near the equator
]


@pytest.mark.parametrize(
    "address, expected_latitude, expected_longitude, expected_score", test_cases
)
def test_fetch_coordinates_parameterized(
    mocker, address, expected_latitude, expected_longitude, expected_score
):
    mocked_response = mocker.Mock()
    mocked_response.status_code = HTTPStatus.OK
    mocked_response.json.return_value = {
        "features": [
            {
                "geometry": {"coordinates": [expected_longitude, expected_latitude]},
                "properties": {"score": expected_score},
            }
        ]
    }

    mocker.patch(
        "network_coverage_api.app.data_processing.requests.get",
        return_value=mocked_response,
    )
    exc = None
    try:
        coordinate = fetch_coordinates(address)
    except HTTPException as exc:
        exception = exc
        coordinate = None

    if expected_latitude is None:
        assert coordinate is None
        assert exception.status_code == 404
        assert exception.detail == "Incorrect address found"
    else:
        assert getattr(coordinate, "longitude", None) == expected_longitude
        assert getattr(coordinate, "latitude", None) == expected_latitude
        assert getattr(coordinate, "score", None) == expected_score


network_coverage_df = pd.DataFrame(
    {
        "longitude": [2.380383, 2.385, 2.390, 2.395],
        "latitude": [48.860248, 48.862, 48.864, 48.866],
        "provider": ["Orange", "SFR", "Bouygue", "Free"],
    }
)


def test_find_network_coverage_data():
    coordinate = ApiAdresseResponse(longitude=2.385, latitude=48.862, score=0.5)
    tolerance = 0.005
    result = find_network_coverage_data(network_coverage_df, coordinate, tolerance)
    assert isinstance(result, pd.DataFrame)


def test_find_network_coverage_data_no_match():
    coordinate = ApiAdresseResponse(longitude=2.0, latitude=50.0, score=0.5)
    tolerance = 0.005

    with pytest.raises(HTTPException) as exc_info:
        result = find_network_coverage_data(network_coverage_df, coordinate, tolerance)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Network coverage not found"