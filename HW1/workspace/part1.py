"""
Part 1
Write an application that reads in the logs produced by a web server. For each unique IP, compute the total
number of bytes served to that IP address.
"""
from pyspark import SparkContext
from pyspark.sql import SparkSession
import ipaddress

sc = SparkContext()
spark = SparkSession(sc)
# textFile: read txt file from local
# map: extract the first and fifth term out
# filter: filter out rows that contains '-'
# reduceByKey: sum terms up according to the ip address
output = sc.textFile("epa-http.txt").map(lambda x: (x.split(' ')[0], x.split(' ')[len(x.split(' ')) - 1])) \
    .filter(lambda y: y[1] != '-').reduceByKey(lambda a, b: int(a) + int(b))

# Determine whether the input is an IP address but not a domain
def is_ip_address(addr):
    try:
        ip = ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

# Filter the non-ip address out, and sort by ip address
# In sortBy function, true for ascending
filtered_output = output.filter(lambda x: is_ip_address(str(x[0]))).sortBy(lambda x: str(x[0]), True).map(lambda x: (x[0], int(x[1])))
# print(filtered_output.collect())

# Change data type to dataframe and output to csv file
df = spark.createDataFrame(filtered_output, schema=["IP", "bytes"])
# df.show()
df.coalesce(1).write.option("mapreduce.fileoutputcommitter.marksuccessfuljobs","false").csv('output/part1_output')