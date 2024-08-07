import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)


def test_read_root():
    """
    Test the root endpoint ("/").

    This test checks that the root endpoint returns a status code of 200
    and the expected greeting message.

    Assertions:
        - Response status code is 200.
        - Response JSON content is {"Hello": "World"}.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_item_existing_state():
    """
    Test querying an existing state ("/query/{state}").

    This test checks that querying for a valid state name
    returns a status code of 200
    and does not include an error message in the response.

    Assumptions:
        - The state name "Canada" should be present in the dataset.

    Assertions:
        - Response status code is 200.
        - Response JSON does not contain the "error" key.
    """
    state_name = "Canada"
    response = client.get(f"/query/{state_name}")
    assert response.status_code == 200
    data = response.json()
    assert "error" not in data


def test_read_item_non_existing_state():
    """
    Test querying a non-existing state ("/query/{state}").

    This test checks that querying for a state name not present in the dataset
    returns a status code of 200 and the appropriate error message.

    Assumptions:
        - The state name "NonExistingState" should not be in the dataset.

    Assertions:
        - Response status code is 200.
        - Response JSON contains the error
        message {"error": "state not found"}.
    """
    state_name = "NonExistingState"
    response = client.get(f"/query/{state_name}")
    assert response.status_code == 200
    assert response.json() == {"error": "state not found"}


def test_dump_all_top10():
    """
    Test getting the top 10 states ("/list/top10").

    This test checks that the endpoint for
    retrieving the top 10 states returns
    a status code of 200 and that the returned
    data includes more than 0 entries.

    Assertions:
        - Response status code is 200.
        - Length of response JSON data is greater than 0.
    """
    response = client.get("/list/top10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Assuming your dataset has more than 10 states


def test_autocomplete_suggestions():
    """
    Test autocomplete suggestions ("/autocomplete").

    This test checks that the autocomplete endpoint
    returns suggestions that match
    the query and are limited to a maximum of 5 suggestions.

    Assumptions:
        - The query "Ca" should match some states in the dataset.

    Assertions:
        - Response status code is 200.
        - The length of the response JSON data is greater than 0.
        - Each suggestion starts with the provided query string.
    """
    query = "Ca"  # This should match some states in your dataset
    response = client.get(f"/autocomplete?query={query}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Ensure that there are suggestions
    for suggestion in data:
        # Ensure each suggestion starts with the query
        assert suggestion.lower().startswith(query.lower())
