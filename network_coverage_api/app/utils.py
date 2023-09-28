"""
Utility functions for network coverage API.
"""

import logging

import numpy as np
import pyproj
from pandas import DataFrame


def calculate_tolerance(city_latitude_ref: float, tolerance_in_meters: float) -> float:
    """
    Calculate the combined tolerance (Euclidean distance) given a tolerance in meters and the latitude of the city's reference point.

    :param city_latitude_ref: Latitude of the city's reference point in decimal degrees.
    :param tolerance_in_meters: Tolerance in meters.
    :return: Combined tolerance as a float.
    """
    tolerance_latitude = tolerance_in_meters / 111320
    tolerance_longitude = tolerance_in_meters / (
        111320 * np.cos(np.radians(city_latitude_ref))
    )
    combined_tolerance = np.sqrt(tolerance_latitude**2 + tolerance_longitude**2)
    return combined_tolerance


def convert_lambert93_to_wgs84(point_x: float, point_y: float) -> tuple[float, float]:
    """
    Convert Lambert 93 coordinates (x, y) to WGS84 longitude and latitude.

    :param point_x: Lambert 93 X-coordinate.
    :param point_y: Lambert 93 Y-coordinate.
    :return: Tuple containing (longitude, latitude) in decimal degrees.
    """
    try:
        lambert = pyproj.Proj(
            "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        )
        wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
        longitude, latitude = pyproj.transform(lambert, wgs84, point_x, point_y)
        return longitude, latitude
    except pyproj.exceptions.ProjError as exception:
        logging.error("Error converting Lambert 93 to WGS84: %s", exception)
        return None


def convert_lambert93_df_to_wgs84(dataframe: DataFrame) -> DataFrame:
    """
    Convert a DataFrame containing Lambert 93 coordinates to WGS84 longitude and latitude.

    :param df: DataFrame with 'x' and 'y' columns containing Lambert 93 coordinates.
    :return: DataFrame with additional 'longitude' and 'latitude' columns in decimal degrees.
    """
    try:
        lambert = pyproj.Proj(
            "+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
        )
        wgs84 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
        dataframe["longitude"], dataframe["latitude"] = pyproj.transform(
            lambert, wgs84, dataframe["x"], dataframe["y"]
        )
        return dataframe
    except pyproj.exceptions.ProjError as exception:
        logging.error("Error converting Lambert 93 to WGS84: %s", exception)
        return None
