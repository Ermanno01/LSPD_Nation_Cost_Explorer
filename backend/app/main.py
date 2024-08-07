"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from app.mymodules.cost_of_living import Cost_of_living
import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8082",
        "http://localhost",
        "http://frontend_nce"
        ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Initialize the Cost_of_living object with the path to the CSV file
csv_path = os.path.join(os.path.dirname(__file__),
                        'mymodules', 'data', 'Cost_of_Living_Index_2022.csv')
state_data = Cost_of_living(csv_path)


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting message.
    """
    return {"Hello": "World"}


@app.get('/query/{state}')
def read_item(state: str):
    """
    Endpoint to query state data based on the state name.

    Args:
        state (str): The name of the state to query.

    Returns:
        dict: Cost information for the provided state.
              If the state is not found, returns an error message.
    """
    state_info = state_data.getState(state)
    return state_info


@app.get('/list/top10')
def dump_all_top10():
    """
    Endpoint to get the top 10 states based on the cost of living index.

    Returns:
        list: A list of dictionaries containing
        the top 10 states and their cost of living index.
    """
    data = state_data.getTop10()
    # If getTop10() returns a JSON string,
    # load it into a Python list/dictionary
    if isinstance(data, str):
        data = json.loads(data)
    return data


@app.get('/autocomplete')
def autocomplete(query: str = Query(None, min_length=1)):
    """
    Endpoint to get state suggestions based on the user's input.

    Args:
        query (str): The input string to filter state names by.

    Returns:
        JSONResponse: A JSON response containing a
        list of up to 5 state names that start with the given query.
    """
    res = state_data.getCountries()
    filtered_suggestions = [
        s for s in res if s.lower().startswith(query.lower())][:5]
    return JSONResponse(content=filtered_suggestions)
