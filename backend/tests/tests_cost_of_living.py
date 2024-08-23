import pytest
import pandas as pd
import os
from app.mymodules.cost_of_living import Cost_of_living

@pytest.fixture
def valid_file_path():
    # Create a sample CSV file for testing
    data = {
        'Country': ['TestState1', 'TestState2'],
        'Some Column': [1, 2],
        'Cost of Living Plus Rent Index': [100, 200]
    }
    file_path = 'test_cost_of_living.csv'
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    yield file_path
    os.remove(file_path)  # Clean up after test

@pytest.fixture
def cost_of_living(valid_file_path):
    return Cost_of_living(valid_file_path)

def test_initialization_success(valid_file_path):
    # Test successful initialization with a valid file
    cost_of_living = Cost_of_living(valid_file_path)
    assert not cost_of_living.df.empty

def test_initialization_file_not_found(monkeypatch):
    """
    Test for handling FileNotFoundError when the CSV file does not exist.
    """
    invalid_file_path = 'non_existent_file.csv'
    full_path = os.path.abspath(invalid_file_path)
    
    # Mock the error_handler method to verify that it is called
    def mock_error_handler(message):
        assert message == f"File not found: {full_path}"
    
    monkeypatch.setattr(Cost_of_living, '_default_error_handler', mock_error_handler)
    
    # Ensure the exception is raised
    with pytest.raises(FileNotFoundError) as exc_info:
        Cost_of_living(invalid_file_path)
    
    # Check the exception message
    exception_message = str(exc_info.value)
    expected_message = f"File not found: {full_path}"
    assert exception_message == expected_message, f"Expected '{expected_message}' but got '{exception_message}'"

def test_get_state(cost_of_living):
    # Test for an existing state
    result = cost_of_living.getState('TestState1')
    assert len(result) == 1
    assert result[0]['Cost of Living Plus Rent Index'] == 100

def test_get_state_not_found(cost_of_living):
    # Test for a non-existing state
    result = cost_of_living.getState('NonExistentState')
    assert result == {'error': 'state not found'}

def test_get_top10(cost_of_living):
    # Test for the top 10 states
    result = cost_of_living.getTop10()
    assert result is not None
    assert isinstance(result, str)  # Ensure it returns a JSON string
    # Optionally, parse the JSON and check contents
    data = pd.read_json(result)
    assert len(data) <= 10  # Ensure it doesn't exceed 10 records

def test_get_countries(cost_of_living):
    # Test for getting all countries
    result = cost_of_living.getCountries()
    assert 'TestState1' in result.values
    assert 'TestState2' in result.values
