from flask import Flask, render_template, request
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuration for the FastAPI backend URL
# Replace with the actual URL of your FastAPI backend
FASTAPI_BACKEND_HOST = 'http://backend_nce:8000'
print(FASTAPI_BACKEND_HOST)

BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class QueryForm(FlaskForm):
    state_name = StringField('State Name:')
    submit = SubmitField('Search')


@app.route('/')
def index():
    """
    Render the index page and display
    the top 10 countries' cost of living data.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    top10_data = fetch_top10_from_backend()
    return render_template('index.html', top10_data=top10_data, form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Render the search page and display the state data.

    Returns:
        str: Rendered HTML content for the search page.
    """
    form = QueryForm()
    state_data = None

    if form.validate_on_submit():
        state_name = form.state_name.data
        state_data = fetch_state_data_from_backend(state_name)

    return render_template('index.html', form=form, state_data=state_data)


def fetch_top10_from_backend():
    """
    Fetch the top 10 countries' cost of living data from the backend.

    Returns:
        list: List of dictionaries containing the top 10 countries' data.
    """
    fastapi_url = f'{FASTAPI_BACKEND_HOST}/list/top10'
    try:
        response = requests.get(fastapi_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top 10 data from backend: {e}")
        return []


def fetch_state_data_from_backend(state_name):
    """
    Fetch state data from the backend.

    Args:
        state_name (str): Name of the state.

    Returns:
        dict: State data or an error message.
    """
    fastapi_url = f'{BACKEND_URL}{state_name}'
    try:
        response = requests.get(fastapi_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching state data from backend: {e}")
        return {'error': 'State not found'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)