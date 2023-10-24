from pyspark import SparkContext
import time
import matplotlib.pyplot as plot
import random
import numpy as np
from pyspark.sql import SQLContext

sc = SparkContext("local", "myApp")
sqlContext = SQLContext(sc)

NUMBER_INPUT = 100000
load_factor_list = [random.randint(1, 100) for i in range(NUMBER_INPUT)]
lf_list_RDD = sc.parallelize(load_factor_list).map(lambda x: int(x))
X = [float(i) * 0.01 for i in range(100)]
Y = [1 for i in range(100)]
X_reorder = X
Y_reorder = []
for selectivity in range(100):
    start_a1 = time.time()
    # Filter out even number, keep selectivity 50%
    list_a = lf_list_RDD.filter(lambda x: x % 2 == 1)
    end_a1 = time.time()
    # Keep selectivity as chosen
    start_a2 = time.time()
    list_a1 = list_a.filter(lambda x: x < selectivity)
    end_a2 = time.time()
    throughput_origin = (end_a1 - start_a1) + (end_a2 - start_a2) * 0.5

    start_b1 = time.time()
    # Filter out even number, keep selectivity 50%
    list_c = lf_list_RDD.filter(lambda x: x < selectivity)
    end_b1 = time.time()
    # Keep selectivity as chosen
    start_b2 = time.time()
    list_c1 = list_c.filter(lambda x: x % 2 == 1)
    end_b2 = time.time()
    throughput_reordered = (end_b1 - start_b1) + (end_b2 - start_b2) * selectivity/100
    Y_reorder.append(throughput_origin / throughput_reordered)
plot.plot(X, Y, color='blue', label="Origin")
plot.plot(X_reorder, Y_reorder, color='red', label="Re-ordered")
plot.xlabel('Selectivity of B')
plot.ylabel('Throughput')
plot.title('Selection Reordering')
plot.legend()
plot.savefig('Operator_Reordering_Result.png')
