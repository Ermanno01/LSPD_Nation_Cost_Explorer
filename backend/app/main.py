"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""
from app.mymodules.cost_of_living import Cost_of_living
# from .mymodules/cost_of_living import *
from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# state_data = Cost_of_living('./data/Cost_of_Living_Index_2022.csv')
app = FastAPI()


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


@app.get('/query/top10')
def dump_all_top10():
    return state_data.getTop10()
