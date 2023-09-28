import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, Query

from network_coverage_api.app.data_processing import (
    create_network_coverage_response,
    fetch_coordinates,
    find_network_coverage_data,
)
from network_coverage_api.app.utils import calculate_tolerance

router = APIRouter()

load_dotenv()

CSV_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "../data", "network_data_cleaned.csv"
)


@router.get("/network-coverage/")
async def get_network_coverage(
    address: str = Query(..., description="Textual address")
):
    search_address_api_url = os.getenv("SEARCH_ADDRESS_API_URL")
    search_address_api_url = search_address_api_url.format(q=address)
    coordinate = fetch_coordinates(search_address_api_url)

    LATITUDE_REF = 48.860248
    TOLERANCE_IN_METERS = 500
    tolerance = calculate_tolerance(LATITUDE_REF, TOLERANCE_IN_METERS)
    tolerance = round(tolerance, 4)

    print(coordinate.longitude, coordinate.latitude)

    network_coverage_df = pd.read_csv(CSV_FILE_PATH, sep=",")
    coverage_results = find_network_coverage_data(
        network_coverage_df, coordinate, tolerance
    )

    response_data = create_network_coverage_response(coverage_results)

    return response_data
