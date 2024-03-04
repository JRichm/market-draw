import csv
import pygame
from datetime import datetime
import math

# initialize pygame
pygame.init()


# setup display
width, height = 800, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Stock Close Prices with Buy/Sell Indicators")

# define colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# read csv file
csv_file_path = "MSFT.csv"
data = []

# fill data array
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    for row in csv_reader:
        data.append(row)


# get dates and close prices from data
dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
close_prices = [float(row[4]) for row in data]


# function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))


def knn_prediction(data, query_point, k):
    distances = [(euclidean_distance(query_point, x), label) for x, label in data]
    sorted_distances = sorted(distances, key=lambda x: x[0])
    k_nearest_neighbors = sorted_distances[:k]
    lables = [neighbor[1] for neighbor in k_nearest_neighbors]
    prediction = max(set(lables), key = lables.count) # choose the label with the majority vote
    return prediction


# preprocess data into features and labels
features_labels = [
    ([float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6])],  # features
    1 if close_prices[i] < close_prices[i + 1] else -1)  # label: 1 for buy, else -1 for sell
    for i, row in enumerate(data[:-1])
]


# perform k-NN predictions for all data points
k = 3 # number of neighbors to consider
predictions = [knn_prediction(features_labels, features, k) for features, _ in features_labels]


# setup pygame clock
clock = pygame.time.Clock()


# main loop
running = True
zoom_factor = 1.0  # Initial zoom factor

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Move left
                zoom_factor *= 1.1
                print("pan left")
            elif event.key == pygame.K_RIGHT:
                # Move right
                zoom_factor /= 1.1
                print("pan right")
            elif event.key == pygame.K_DOWN:
                # Zoom out
                zoom_factor /= 1.1
                print("zoom out")
            elif event.key == pygame.K_UP:
                # Zoom in
                zoom_factor *= 1.1
                print("zoom in")

    # Clear the screen
    screen.fill(white)

    # Calculate the visible range based on zoom factor
    visible_range = int(len(dates) / zoom_factor)

    # plot closing prices
    for i in range(1, min(len(dates), visible_range + 1)):
        x = int((i - 1) * zoom_factor)
        price = int(height - close_prices[i - 1] * zoom_factor)
        pygame.draw.line(screen, blue, (x, price), (x + 1, height - close_prices[i] * zoom_factor))

        # Highlight buy (green) and sell (red) indicators
        if predictions[i - 1] == 1:
            alpha_surface = pygame.Surface((1, height), pygame.SRCALPHA)
            alpha_surface.fill((0, 255, 0, 75))
            screen.blit(alpha_surface, (x, 0))
        elif predictions[i - 1] == -1:
            alpha_surface = pygame.Surface((1, height), pygame.SRCALPHA)
            alpha_surface.fill((255, 0, 0, 75))
            screen.blit(alpha_surface, (x, 0))

    pygame.display.flip()
    clock.tick(60)


# quit pygame
pygame.quit()