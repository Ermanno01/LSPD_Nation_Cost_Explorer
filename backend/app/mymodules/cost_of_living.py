import json
import pandas as pd
import os


class Cost_of_living:

    def __init__(self, file_path):
        # print(f"Looking for CSV at: {file_path}")
        # print(os.listdir(file_path))
        # state_data = Cost_of_living(file_path)
        base_dir = os.path.dirname(__file__)
        full_path = os.path.join(base_dir, file_path)
        print(full_path)

        self.df = pd.read_csv(full_path, header=1)

    def getState(self, state_name: str):

        result = self.df[self.df['Country'] == state_name]
        if not result.empty:
            # Return as a list of dictionaries
            return result.to_dict(orient='records')
        else:
            return {'error': "state not found"}  # Return a dictionary directly

    def getTop10(self):
        # Get the top 10 rows based on the 5th column (index 4)
        top_10_rows = self.df.nlargest(10, self.df.columns[4])
        
        # Select only the 1st and 5th columns (index 0 and 4)
        selected_columns = top_10_rows.iloc[:, [1, 4]]
        
        # Convert to JSON format
        return selected_columns.to_json(orient='records')
