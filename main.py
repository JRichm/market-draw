import csv
import matplotlib.pyplot as plt
from datetime import datetime

csv_file = "MSFT.csv"
data = []

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)
    for row in csv_reader:
        data.append(row)


dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
open_prices = [float(row[1]) for row in data]
high_prices = [float(row[2]) for row in data]
low_prices = [float(row[3]) for row in data]
close_prices = [float(row[4]) for row in data]
adj_close_prices = [float(row[5]) for row in data]
volume = [int(row[6]) for row in data]

plt.figure(figsize=(10, 6))
plt.plot(dates, close_prices, label='Close Prices', color='blue')
plt.title("Stock Close Prices Over Time")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.show()