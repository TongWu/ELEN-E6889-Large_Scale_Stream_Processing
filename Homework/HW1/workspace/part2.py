"""
Part 2
Extend the application to return the top-K IPs that were served the most number of bytes.
"""
from pyspark import SparkContext
import ipaddress
from pyspark.sql import SparkSession

sc = SparkContext()
spark = SparkSession(sc)

# textFile: read txt file from local
# map: extract the first and fifth term out
# filter: filter out columns that contains '-'
# reduceByKey: sum terms up according to the ip address
result = sc.textFile("epa-http.txt").map(lambda x: (x.split(' ')[0], x.split(' ')[len(x.split(' ')) - 1])) \
    .filter(lambda y: y[1] != '-').reduceByKey(lambda a, b: int(a) + int(b))
# sortBy: sort the data according to the given row
output_part2 = result.sortBy(lambda x: int(x[1]), False)

# Determine whether the input is an IP address but not a domain
def is_ip_address(addr):
    try:
        ip = ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

# Filter the non-ip address out
filtered_output = output_part2.filter(lambda x: is_ip_address(str(x[0]))).map(lambda x: (x[0], int(x[1])))

# Extracting the top 10 IP address
top_10 = filtered_output.take(10)
# result.take(10)
# print(filtered_output.collect())
df_10 = spark.createDataFrame(top_10, schema=["IP", "bytes"])
# df.show()
df_10.coalesce(1).write.option("mapreduce.fileoutputcommitter.marksuccessfuljobs","false").csv('output/part2_output/top10')

# Extracting the top 100 IP address
top_100 = filtered_output.take(100)
df_100 = spark.createDataFrame(top_100, schema=["IP", "bytes"])
# df.show()
df_100.coalesce(1).write.option("mapreduce.fileoutputcommitter.marksuccessfuljobs","false").csv('output/part2_output/top100')