# filename: download_plot.py

import pandas as pd
import matplotlib.pyplot as plt

# Download the .CSV file
data = pd.read_csv('https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv')

# Print the fields in the CSV file
print(data.columns.tolist())
# (data.columns.tolist(), ">>>>>")

# Plotting
plt.scatter(data['Weight'], data['Horsepower(HP)'])

# Labeling the plot
plt.xlabel('Weight in lbs')
plt.ylabel('Horsepower')
plt.title('Relationship between weight and horsepower')

# Save the plot to a file
plt.savefig('output.png')

print("Plot saved as output.png")