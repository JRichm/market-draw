import csv
import matplotlib.pyplot as plt
from datetime import datetime
import math

# read csv file
csv_file_path = 'MSFT.csv'
data = []

# fill data array
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader) 
    for row in csv_reader:
        data.append(row)

# get dates and close prices from data
dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
close_prices = [float(row[4]) for row in data]

# function to calculate euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y, in zip(point1, point2)))


# function to perform k-NN classification
def knn_prediction(data, query_point, k):
    distances = [(euclidean_distance(query_point, x), label) for x, label in data]
    sorted_distances = sorted(distances, key=lambda x: x[0])
    k_nearest_neighbors = sorted_distances[:k]
    labels = [neighbor[1] for neighbor in k_nearest_neighbors]
    prediction = max(set(labels), key=labels.count) # choose the label with the majority vote
    return prediction

# preprocess data into features and labels
features_labels = [
    ([float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6])], # features
    1 if close_prices[i] < close_prices[i + 1] else -1) # label: 1 for buy, else -1 for sell
    for i, row in enumerate(data[:-1])
]

# perform k-NN predictions for all data points
k = 3 # number of neighbors to consider
predictions = [knn_prediction(features_labels, features, k) for features, _ in features_labels]

# plot closing prices
plt.figure(figsize=(10, 6))
plt.plot(dates[:-1], close_prices[:-1], label='Close Prices', color='blue')

# highlight buy (green) and sell (red) indicators
for i in range(1, len(dates)):
    if predictions[i - 1] == 1:
        plt.axvspan(dates[i - 1], dates[i], facecolor='green', alpha=0.3)
    elif predictions[i - 1] == -1:
        plt.axvspan(dates[i - 1], dates[i], facecolor='red', alpha=0.3)


plt.title('Stock Close Prices with Buy/Sell Indicators')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()