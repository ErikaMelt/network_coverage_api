from typing import Dict, Tuple

import numpy as np
import pandas as pd
import requests
from fastapi import HTTPException

from network_coverage_api.models.network_coverage import \
    NetworkCoverageResponseData


def fetch_coordinates(address_api_url: str) -> Tuple[float, float]:
    response = requests.get(address_api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Address API request failed")

    data = response.json()
    if not data.get("features"):
        raise HTTPException(status_code=404, detail="Address not found")

    #coordinates = data["features"][0]["geometry"]["coordinates"]
    x = data["features"][0]["properties"]["x"]
    y = data["features"][0]["properties"]["y"]
    return x, y


def find_coverage_data(
    network_coverage_df: pd.DataFrame,
    longitude: float,
    latitude: float,
    tolerance: float,
) -> pd.DataFrame:
    results = network_coverage_df[
        (np.isclose(network_coverage_df.x, longitude, atol=tolerance))
        & (np.isclose(network_coverage_df.y, latitude, atol=tolerance))
    ]
    return results


def create_network_coverage_response(
    coverage_results: pd.DataFrame,
) -> Dict[str, NetworkCoverageResponseData]:
    response_data = {}
    for _, row in coverage_results.iterrows():
        operator_name = row["operator_name"]
        coverage = {"2G": bool(row["2G"]), "3G": bool(row["3G"]), "4G": bool(row["4G"])}
        response_data[operator_name] = NetworkCoverageResponseData(coverage=coverage)
    return response_data
