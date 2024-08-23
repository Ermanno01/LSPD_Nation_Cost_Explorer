import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app.mymodules.cost_of_living import Cost_of_living
from app.main import app

client = TestClient(app)

def test_init_file_not_found(monkeypatch):
    """
    Test that initializing Cost_of_living with a non-existent file path
    raises a FileNotFoundError.

    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest fixture to modify 
        the behavior of methods or attributes for the test.
    """
    fake_file_path = "/app/app/mymodules/non_existent_file.csv"

    monkeypatch.setattr(os.path, "isfile", lambda x: False)

    with pytest.raises(FileNotFoundError) as exc_info:
        obj = Cost_of_living(fake_file_path)

    expected_message = f"File not found: {os.path.join(os.path.dirname(__file__), fake_file_path)}"
    assert str(exc_info.value) == expected_message
