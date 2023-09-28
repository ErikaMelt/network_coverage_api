from typing import Dict

import numpy as np
import pandas as pd
import requests
from fastapi import HTTPException
from scipy.spatial.distance import cdist

from network_coverage_api.models.api_addrese_response import ApiAdresseResponse
from network_coverage_api.models.network_coverage import \
    NetworkCoverageResponseData


def fetch_coordinates(address_api_url: str) -> ApiAdresseResponse:
    """
    Fetches coordinates (longitude and latitude) from an address API.

    Args:
        address_api_url (str): The URL of the address API.

    Returns:
        ApiAdresseResponse: An object with the longitude and latitude and score.

    Raises:
        HTTPException: If the address API request fails or the address is not found.
    """
    response = requests.get(address_api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Address API request failed")

    data = response.json()
    features = data.get("features")
    if not features:
        raise HTTPException(status_code=404, detail="Address not found")

    geometry = features[0]["geometry"]["coordinates"]
    properties = features[0].get("properties", {})
    score = properties.get("score", 0.0)

    longitude = geometry[0]
    latitude = geometry[1]

    print(longitude, latitude, score)

    if score is not None and score < 0.4:
        raise HTTPException(status_code=404, detail="Incorrect address found")

    if not isinstance(longitude, (float, int)) or not isinstance(
        latitude, (float, int)
    ):
        raise HTTPException(status_code=404, detail="Incorrect address found")

    return ApiAdresseResponse(longitude=longitude, latitude=latitude, score=score)


def find_network_coverage_data(
    network_coverage_df: pd.DataFrame,
    coordinate: ApiAdresseResponse,
    tolerance: float,
) -> pd.DataFrame:
    """
    Finds network coverage data based on longitude and latitude within a specified tolerance.

    Args:
        network_coverage_df (pd.DataFrame): The DataFrame containing network coverage data.
        ApiAdresseResponse: the longitude and The latitude of the target location.
        tolerance (float): The tolerance in meters for matching.

    Returns:
        pd.DataFrame: A DataFrame containing the closest points within the tolerance.

    """
    match_within_tolerance = network_coverage_df[
        (
            np.isclose(
                network_coverage_df.longitude, coordinate.longitude, atol=tolerance
            )
        )
        & (
            np.isclose(
                network_coverage_df.latitude, coordinate.latitude, atol=tolerance
            )
        )
    ]
    if len(match_within_tolerance) == 0:
        raise HTTPException(status_code=404, detail="Network coverage not found")

    closest_points = select_closest_points(coordinate, match_within_tolerance)

    if len(closest_points) == 0:
        raise HTTPException(
            status_code=404, detail="Not closest point network coverage found"
        )

    return closest_points


def select_closest_points(
    coordinate: ApiAdresseResponse,
    matches_within_tolerance: pd.DataFrame,
    TOP_MATCHES=5,
) -> pd.DataFrame:
    """
    Selects the N closest points to a target longitude and latitude.

    Args:
        ApiAdresseResponse with the latitude, longitude of the target
        matches_within_tolerance (pd.DataFrame): DataFrame of matching points within tolerance.
        N (int): The number of closest points to select.

    Returns:
        pd.DataFrame: A DataFrame containing the closest N points.
    """
    target_coords = np.array([[coordinate.longitude, coordinate.latitude]])

    matched_coords = matches_within_tolerance[["longitude", "latitude"]].values
    distances = cdist(target_coords, matched_coords, metric="cityblock")

    result_df = matches_within_tolerance.copy()
    result_df["distance"] = distances[0]

    closest_matches = result_df.sort_values(by="distance")
    closest_points = closest_matches.head(TOP_MATCHES)

    return closest_points


def create_network_coverage_response(
    coverage_results: pd.DataFrame,
) -> Dict[str, NetworkCoverageResponseData]:
    """
    Creates a response containing network coverage data.

    Args:
        coverage_results (pd.DataFrame): DataFrame containing network coverage results.

    Returns:
        Dict[str, NetworkCoverageResponseData]: A dictionary with operator names as keys
        and NetworkCoverageResponseData as values.
    """
    response_data = {}
    for _, row in coverage_results.iterrows():
        operator_name = row["operator_name"]
        coverage = {"2G": bool(row["2G"]), "3G": bool(row["3G"]), "4G": bool(row["4G"])}
        response_data[operator_name] = NetworkCoverageResponseData(coverage=coverage)
    return response_data
