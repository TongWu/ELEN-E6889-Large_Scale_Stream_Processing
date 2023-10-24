from pyspark import SparkContext
import time
from datetime import datetime
import matplotlib.pyplot as plot
import random

sc = SparkContext("local", "myApp")

# Initialize the data and window size
NUMBER_INPUT = 1000
window_size_arr = [1, 200, 400, 600, 800, 1000]
list1 = sc.parallelize([(i % 100, i) for i in range(NUMBER_INPUT)])
list2 = sc.parallelize([(i % 100, i * 10) for i in range(NUMBER_INPUT)])


def hash(window_size):
    start = time.time()
    result = (list1.join(list2).reduceByKey(lambda x, y: x + y).filter(lambda x: x[0] < window_size).map(lambda x: x[1])
              .reduce(lambda x, y: x + y))
    end = time.time()
    return end - start


def nested(window_size):
    start = time.time()
    result = (list1.cartesian(list2).filter(lambda x: x[0][0] == x[1][0]).reduceByKey(lambda x, y: x + y)
              .filter(lambda x: x[0][0] < window_size).map(lambda x: x[1]).reduce(lambda x, y: x + y))
    end = time.time()
    return end - start


# Initialization
hash_times = []
nested_times = []
Y = [1 for i in range(6)]
# Loop for different window size
for window_size in window_size_arr:
    hash_times.append(hash(window_size))
    nested_times.append(nested(window_size))

# Calculate throughput
records = list1.count()
nested_throughput = [records / t for t in nested_times]

# Plot the diagram
plot.plot(window_size_arr, Y, color='red', label="Hash Join")
norm = [(nested_throughput[i] - min(nested_throughput)) / (max(nested_throughput) - min(nested_throughput)) for i in
        range(len(nested_throughput))]
plot.plot(window_size_arr, norm, color='blue', label="Nested Loop Join")
plot.ylabel('Throughput')
plot.xlabel('Window Size')
plot.title('Algorithm Selection')
plot.legend()
plot.savefig('Algorithm_Selection_Result.png')