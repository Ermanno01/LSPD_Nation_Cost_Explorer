"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""
from fastapi import FastAPI
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
    allow_origins=["http://127.0.0.1", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# state_data = Cost_of_living('./data/Cost_of_Living_Index_2022.csv')


csv_path = os.path.join(os.path.dirname(__file__),
                        'mymodules', 'data', 'Cost_of_Living_Index_2022.csv')
state_data = Cost_of_living(csv_path)


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}


@app.get('/query/{state}')
def read_item(state: str):
    """
    Endpoint to query state data based on state.

    Args:
        state (str): The name of the state.

    Returns:
        dict: Cost information for the provided state.
    """

    state_info = state_data.getState(state)
    return state_info


@app.get('/list/top10')
def dump_all_top10():
    data = state_data.getTop10()
    # If getTop10() returns a JSON string, load it into a Python list/dictionary
    if isinstance(data, str):
        data = json.loads(data)
    return data

