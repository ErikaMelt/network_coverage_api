from typing import Dict, Tuple

import numpy as np
import pandas as pd
import requests
from fastapi import HTTPException
from scipy.spatial.distance import cdist

from network_coverage_api.models.network_coverage import \
    NetworkCoverageResponseData


def fetch_coordinates(address_api_url: str) -> Tuple[float, float]:
    """
    Fetches coordinates (longitude and latitude) from an address API.

    Args:
        address_api_url (str): The URL of the address API.

    Returns:
        Tuple[float, float]: A tuple containing the longitude and latitude.

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
    longitude = geometry[0]
    latitude = geometry[1]

    return longitude, latitude


def find_coverage_data(
    network_coverage_df: pd.DataFrame,
    longitude: float,
    latitude: float,
    tolerance: float,
) -> pd.DataFrame:
    """
    Finds network coverage data based on longitude and latitude within a specified tolerance.

    Args:
        network_coverage_df (pd.DataFrame): The DataFrame containing network coverage data.
        longitude (float): The longitude of the target location.
        latitude (float): The latitude of the target location.
        tolerance (float): The tolerance in meters for matching.

    Returns:
        pd.DataFrame: A DataFrame containing the closest points within the tolerance.

    """
    match_within_tolerance = network_coverage_df[
        (np.isclose(network_coverage_df.longitude, longitude, atol=tolerance))
        & (np.isclose(network_coverage_df.latitude, latitude, atol=tolerance))
    ]
    closest_points = select_closest_points(longitude, latitude, match_within_tolerance)
    return closest_points


def select_closest_points(
    longitude: float,
    latitude: float,
    matches_within_tolerance: pd.DataFrame,
    TOP_MATCHES=5,
) -> pd.DataFrame:
    """
    Selects the N closest points to a target longitude and latitude.

    Args:
        longitude (float): The target longitude.
        latitude (float): The target latitude.
        matches_within_tolerance (pd.DataFrame): DataFrame of matching points within tolerance.
        N (int): The number of closest points to select.

    Returns:
        pd.DataFrame: A DataFrame containing the closest N points.
    """
    target_coords = np.array([[longitude, latitude]])

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
