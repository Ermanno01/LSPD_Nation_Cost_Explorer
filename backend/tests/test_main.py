import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_item_existing_state():
    # Replace 'Existing State' with a valid state name from your dataset
    state_name = "Canada"
    response = client.get(f"/query/{state_name}")
    assert response.status_code == 200
    data = response.json()
    assert "error" not in data


def test_read_item_non_existing_state():
    state_name = "NonExistingState"
    response = client.get(f"/query/{state_name}")
    assert response.status_code == 200
    assert response.json() == {"error": "state not found"}


def test_dump_all_top10():
    response = client.get("/query/top10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Assuming your dataset has more than 10 states
