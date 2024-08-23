import pandas as pd
import os

class Cost_of_living:
    """
    A class to handle cost of living data from a CSV file.

    Attributes:
        df (pd.DataFrame): DataFrame containing the cost of living data.
    """

    def __init__(self, file_path):
        """
        Initializes the Cost_of_living instance by loading the CSV file.

        Args:
            file_path (str): Path to the CSV file containing cost of living data.
        """
        self.df = self._load_data(file_path)

    def _load_data(self, file_path):
        """
        Loads the data from the specified CSV file.

        Args:
            file_path (str): Path to the CSV file containing cost of living data.

        Raises:
            FileNotFoundError: If the specified file does not exist.

        Returns:
            pd.DataFrame: DataFrame containing the cost of living data.
        """
        base_dir = os.path.dirname(__file__)
        full_path = os.path.join(base_dir, file_path)
        print(f"Full path for file: {full_path}")

        if not os.path.isfile(full_path):
            # Check if the file exists before attempting to read
            raise FileNotFoundError(f"File not found: {full_path}")

        return pd.read_csv(full_path, header=1)

    def getState(self, state_name: str):
        """
        Retrieves cost of living data for a specific state.

        Args:
            state_name (str): The name of the state to retrieve data for.

        Returns:
            dict: A dictionary containing the cost of living data for the specified state,
                  or an error message if the state is not found.
        """
        result = self.df[self.df['Country'] == state_name]
        if not result.empty:
            return result.iloc[:, 2:].to_dict(orient='records')
        else:
            return {'error': "state not found"}

    def getTop10(self):
        """
        Retrieves the top 10 states based on a specific cost of living index.

        Returns:
            str: A JSON string containing the top 10 states and their cost of living index.
        """
        top_10_rows = self.df.nlargest(10, self.df.columns[4])
        selected_columns = top_10_rows.iloc[:, [1, 4]]
        return selected_columns.to_json(orient='records')

    def getCountries(self):
        """
        Retrieves a list of all countries (states) from the data.

        Returns:
            pd.Series: A Series containing the names of all countries (states).
        """
        return self.df['Country']
