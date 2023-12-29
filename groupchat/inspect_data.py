# filename: inspect_data.py

import pandas as pd

# Download the .CSV file
data = pd.read_csv('https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv')

# Print the first few rows of the dataset to understand its structure
print(data.head())