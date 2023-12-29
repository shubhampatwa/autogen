# filename: plot_data.py

import pandas as pd
import matplotlib.pyplot as plt

# Download the .CSV file
data = pd.read_csv('https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv')

# Plotting
plt.scatter(data['Weight'], data['Horsepower'])

# Labeling the plot
plt.xlabel('Weight')
plt.ylabel('Horsepower')
plt.title('Relationship between weight and horsepower')

# Save the plot to a file
plt.savefig('output.png')

print("Plot saved as output.png")