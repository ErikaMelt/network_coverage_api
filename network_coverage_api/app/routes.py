import logging
import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query

from network_coverage_api.app.data_processing import (
    create_network_coverage_response, fetch_coordinates, find_coverage_data)
from network_coverage_api.app.utils import calculate_tolerance

router = APIRouter()

load_dotenv()

CSV_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "../data", "network_data_cleaned.csv"
)
search_address_api_url = os.getenv("SEARCH_ADDRESS_API_URL")


@router.get("/network-coverage/")
async def get_network_coverage(
    address: str = Query(..., description="Textual address")
):
    try:
        search_address_api_url = search_address_api_url.format(q=address)
        coordinates = fetch_coordinates(search_address_api_url)
        longitude, latitude = coordinates
        print(longitude, latitude)

        LATITUDE_PARIS = 48.860248
        TOLERANCE_IN_METERS = 500
        tolerance = calculate_tolerance(LATITUDE_PARIS, TOLERANCE_IN_METERS)
        tolerance = round(tolerance, 4)

        # Find coverage data
        network_coverage_df = pd.read_csv(CSV_FILE_PATH, sep=",")
        coverage_results = find_coverage_data(
            network_coverage_df, longitude, latitude, tolerance
        )

        response_data = create_network_coverage_response(coverage_results)

        return response_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Resource not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid request")
    except Exception as exception:
        logging.error("Internal Server Error: %s", exception)
        raise HTTPException(status_code=500, detail="Internal Server Error")
