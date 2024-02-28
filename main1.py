import csv
import datetime
import math

csv_file = 'MSFT.csv'
data = []

with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    for row in csv_reader:
        data.append(row)

# extract data columns
dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d') for row in data]
close_prices = [float(row[4]) for row in data]

# function to calculate euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

# function to perform k-NN classification
def knn_predict(data, query_point, k):
    distances = [(euclidean_distance(query_point, x), label) for x, label in data]
    sorted_distances = sorted(distances, key=lambda x: x[0])
    k_nearest_neighbors = sorted_distances[:k]
    labels = [neighbor[1] for neighbor in k_nearest_neighbors]
    prediction = max(set(labels), key=labels.count)
    return prediction 

# preprocess data into features and labels
features_labels = [
    ([float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6])], # features
    1 if close_prices[i] < close_predict[i + 1] else -1)   # label: 1 for buy, -1 for sell
    for i, row in enumerate(data[:-1]) # exclude the last row as we need pairs of data points
]


query_point_index = 100 # replace with the index of the data point you want to predict
query_point = features_labels[query_point_index][0]

k = 3 # number of neighbors to consider
prediction = knn_predict(features_labels, query_point, k)

print(f"Prediction for {dates[query_point_index]}: {'Buy' if prediction == 1 else 'Sell'}")