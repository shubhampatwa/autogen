# filename: plot_stock_price.py

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

# Get the date for the start of the year
start_of_year = datetime.today().strftime('%Y-01-01')

# Download the historical data for META and TESLA
meta_data = yf.download('META', start=start_of_year, end=today)
tesla_data = yf.download('TSLA', start=start_of_year, end=today)

# Plot the closing prices of META and TESLA
plt.figure(figsize=(14, 7))
plt.plot(meta_data['Close'], label='META')
plt.plot(tesla_data['Close'], label='TESLA')
plt.title('Stock Price Change YTD for META and TESLA')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()

# Save the plot to a PNG file
plt.savefig('stock_price_ytd.png')