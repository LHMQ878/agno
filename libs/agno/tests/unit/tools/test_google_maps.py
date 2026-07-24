"""Unit tests for Google Maps tools."""

import json
from datetime import datetime
from unittest.mock import patch

import pytest

from agno.tools.google.maps import GoogleMapsTools

MOCK_DIRECTIONS_RESPONSE = [
    {
        "legs": [
            {
                "distance": {"text": "5 km", "value": 5000},
                "duration": {"text": "10 mins", "value": 600},
                "steps": [],
            }
        ]
    }
]

MOCK_ADDRESS_VALIDATION_RESPONSE = {
    "result": {
        "verdict": {"validationGranularity": "PREMISE", "hasInferredComponents": False},
        "address": {"formattedAddress": "123 Test St, Test City, ST 12345"},
    }
}

MOCK_GEOCODE_RESPONSE = [
    {
        "formatted_address": "123 Test St, Test City, ST 12345",
        "geometry": {"location": {"lat": 40.7128, "lng": -74.0060}},
    }
]

MOCK_DISTANCE_MATRIX_RESPONSE = {
    "rows": [
        {
            "elements": [
                {
                    "distance": {"text": "5 km", "value": 5000},
                    "duration": {"text": "10 mins", "value": 600},
                }
            ]
        }
    ]
}

MOCK_ELEVATION_RESPONSE = [{"elevation": 100.0}]

MOCK_TIMEZONE_RESPONSE = {
    "timeZoneId": "America/New_York",
    "timeZoneName": "Eastern Daylight Time",
}


@pytest.fixture
def google_maps_tools():
    """Create a GoogleMapsTools instance with a mock API key."""
    with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "AIzaTest"}):
        with patch("googlemaps.Client"):
            return GoogleMapsTools(all=True)


def test_get_directions(google_maps_tools):
    """Test the get_directions method."""
    with patch.object(google_maps_tools.client, "directions") as mock_directions:
        mock_directions.return_value = MOCK_DIRECTIONS_RESPONSE

        result = json.loads(google_maps_tools.get_directions(origin="Test Origin", destination="Test Destination"))

        assert "routes" in result
        assert result["routes"][0]["legs"][0]["distance"]["value"] == 5000


def test_validate_address(google_maps_tools):
    """Test the validate_address method."""
    with patch.object(google_maps_tools.client, "addressvalidation") as mock_validate:
        mock_validate.return_value = MOCK_ADDRESS_VALIDATION_RESPONSE

        result = json.loads(google_maps_tools.validate_address("123 Test St"))

        assert "validation" in result
        assert "result" in result["validation"]


def test_geocode_address(google_maps_tools):
    """Test the geocode_address method."""
    with patch.object(google_maps_tools.client, "geocode") as mock_geocode:
        mock_geocode.return_value = MOCK_GEOCODE_RESPONSE

        result = json.loads(google_maps_tools.geocode_address("123 Test St"))

        assert "results" in result
        assert result["results"][0]["formatted_address"] == "123 Test St, Test City, ST 12345"


def test_reverse_geocode(google_maps_tools):
    """Test the reverse_geocode method."""
    with patch.object(google_maps_tools.client, "reverse_geocode") as mock_reverse:
        mock_reverse.return_value = MOCK_GEOCODE_RESPONSE

        result = json.loads(google_maps_tools.reverse_geocode(40.7128, -74.0060))

        assert "results" in result
        assert result["results"][0]["formatted_address"] == "123 Test St, Test City, ST 12345"


def test_get_distance_matrix(google_maps_tools):
    """Test the get_distance_matrix method."""
    with patch.object(google_maps_tools.client, "distance_matrix") as mock_matrix:
        mock_matrix.return_value = MOCK_DISTANCE_MATRIX_RESPONSE

        result = json.loads(google_maps_tools.get_distance_matrix(origins=["Origin"], destinations=["Destination"]))

        assert "matrix" in result
        assert result["matrix"]["rows"][0]["elements"][0]["distance"]["value"] == 5000


def test_get_elevation(google_maps_tools):
    """Test the get_elevation method."""
    with patch.object(google_maps_tools.client, "elevation") as mock_elevation:
        mock_elevation.return_value = MOCK_ELEVATION_RESPONSE

        result = json.loads(google_maps_tools.get_elevation(40.7128, -74.0060))

        assert "elevation" in result
        assert result["elevation"][0]["elevation"] == 100.0


def test_get_timezone(google_maps_tools):
    """Test the get_timezone method."""
    with patch.object(google_maps_tools.client, "timezone") as mock_timezone:
        mock_timezone.return_value = MOCK_TIMEZONE_RESPONSE
        test_time = datetime(2024, 1, 1, 12, 0)

        result = json.loads(google_maps_tools.get_timezone(40.7128, -74.0060, test_time))

        assert "timezone" in result
        assert result["timezone"]["timeZoneId"] == "America/New_York"


def test_error_handling(google_maps_tools):
    """Test error handling in various methods."""
    with patch.object(google_maps_tools.client, "directions") as mock_directions:
        mock_directions.side_effect = Exception("API Error")

        result = json.loads(google_maps_tools.get_directions("origin", "destination"))
        assert "error" in result


def test_initialization_without_api_key():
    """Test initialization without API key."""
    with patch.dict("os.environ", clear=True):
        with pytest.raises(ValueError, match="GOOGLE_MAPS_API_KEY is not set"):
            GoogleMapsTools()


def test_default_tools_enabled():
    """Test that only core tools are enabled by default."""
    with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "AIzaTest"}):
        with patch("googlemaps.Client"):
            tools = GoogleMapsTools()
            tool_names = [f.name for f in tools.functions.values()]

            # Core tools enabled by default
            assert "get_directions" in tool_names
            assert "geocode_address" in tool_names
            assert "reverse_geocode" in tool_names

            # Specialized tools disabled by default
            assert "validate_address" not in tool_names
            assert "get_distance_matrix" not in tool_names
            assert "get_elevation" not in tool_names
            assert "get_timezone" not in tool_names


def test_all_flag_enables_all_tools():
    """Test that all=True enables all tools."""
    with patch.dict("os.environ", {"GOOGLE_MAPS_API_KEY": "AIzaTest"}):
        with patch("googlemaps.Client"):
            tools = GoogleMapsTools(all=True)
            tool_names = [f.name for f in tools.functions.values()]

            assert "get_directions" in tool_names
            assert "geocode_address" in tool_names
            assert "reverse_geocode" in tool_names
            assert "validate_address" in tool_names
            assert "get_distance_matrix" in tool_names
            assert "get_elevation" in tool_names
            assert "get_timezone" in tool_names
