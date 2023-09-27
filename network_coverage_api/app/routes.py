import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, Query

from network_coverage_api.app.data_processing import (
    fetch_coordinates, find_coverage_data, create_network_coverage_response)

router = APIRouter()

load_dotenv()

#TOLERANCE = 0.001
TOLERANCE = 100
csv_file_path = os.path.join(
    os.path.dirname(__file__), "../data", "network_data_cleaned.csv"
)
network_coverage_df = pd.read_csv(csv_file_path, sep=",")


@router.get("/network-coverage/")
async def get_network_coverage(
    address: str = Query(..., description="Textual address")
):
    search_address_api_url = os.getenv("SEARCH_ADDRESS_API_URL")
    search_address_api_url = search_address_api_url.format(q=address)

    coordinates = fetch_coordinates(search_address_api_url)

    x, y = coordinates

    print(f'coordinates: {x, y}')

    coverage_results = find_coverage_data(
        network_coverage_df, x, y, TOLERANCE
    )
    response_data = create_network_coverage_response(coverage_results)

    return response_data
