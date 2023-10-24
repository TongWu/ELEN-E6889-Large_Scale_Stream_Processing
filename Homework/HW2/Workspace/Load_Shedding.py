import numpy as np
import time
from pyspark import SparkContext
import matplotlib.pyplot as plot
import random
from pyspark.sql.functions import desc
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, sum, sqrt

NUMBER_INPUT = 100000
sc = SparkContext("local", "myApp")
sqlContext = SQLContext(sc)

# Initialisation
throughput_arr = []
selectivity_arr = []
error = []
accuracy = []
load_factor = np.arange(1, 10, 0.1)

for i in load_factor:
    load_factor_list = []
    for j in range(int(i * NUMBER_INPUT)):
        load_factor_list.append(random.randint(1, 100))
    lf_list_RDD = sc.parallelize(load_factor_list)

    # Load shedding
    start = time.time()
    # Calculate the selectivity
    selectivity = NUMBER_INPUT / lf_list_RDD.count()
    # Filter the list to selectivity
    normal_list = lf_list_RDD.filter(lambda x: random.random() < selectivity)
    # Add load to the list
    loaded_list = normal_list.map(lambda x: x * 0.02)
    end = time.time()
    throughput = lf_list_RDD.count() / (end - start)

    # Insert data
    throughput_arr.append(throughput)
    selectivity_arr.append(selectivity)

    # Insert zero in order to calculate error
    map_line_list = loaded_list.collect()
    for j in range(len(load_factor_list) - len(map_line_list)):
        map_line_list.append(0)
    # Calculate error

    error.append(np.linalg.norm(np.array(map_line_list) - np.array(load_factor_list)))

norm_error = [(error[i] - min(error)) / (max(error) - min(error)) for i in range(len(error))]
for i in range(len(norm_error)):
    accuracy.append(1 - norm_error[i])
norm_throughput = [(throughput_arr[i] - min(throughput_arr)) / (max(throughput_arr) - min(throughput_arr)) for i in
                   range(len(throughput_arr))]

plot.plot(selectivity_arr, norm_throughput, color='green', label="Throughput")
plot.plot(selectivity_arr, accuracy, color='blue', label="Accuracy")
plot.xlabel('Selectivity')
plot.title('Load Shedding')
plot.legend()
plot.savefig('Load_Shedding_Result.png')
