"""
Part 4
Modify the application to compute the same statistics for a subnet, i.e. aggregate across IPs based on a
specified prefix. For instance, given that an IP (v4) address is 4 bytes, can you aggregate all data for IPs with the
same first 3 bytes (MSB to LSB). As an example, aggregate bytes for all IP addresses that start with 123.100.099.*,
i.e the last three digits can be anything.

csv file with for subnet xxx.xxx.*.* with format:
Subnet,bytes
Sort by subnet in string ascending order so 100.*.*.* comes before 99.*.*.*
"""

from pyspark import SparkContext
from pyspark.sql import SparkSession
import ipaddress
sc = SparkContext()
spark = SparkSession(sc)

# Determine whether the input is an IP address but not a domain
def is_ip_address(addr):
    try:
        ip = ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

# Extract the tuple <IP, bytes>, filter out all domains
result = sc.textFile('epa-http.txt').map(lambda x: (x.split(' ')[0], x.split(' ')[len(x.split(' ')) - 1]))\
    .filter(lambda x: x[1] != '-').filter(lambda x: is_ip_address(str(x[0])))
# Create dataframe to extract the subnet, since no ordering is requested in printing section, so no sortBy()
part4_df = spark.createDataFrame(result, ["ip", "bytes"])
prefixes = part4_df.rdd.map(lambda x: (x[0].rsplit(".", 1)[0], x[1])).reduceByKey(lambda x, y: int(x) + int(y))
# Print the tuple
prefixes.take(10)

# Output tuple <subnet, bytes> to csv file, the subnet is xxx.xxx.*.*
prefixes_output = part4_df.rdd.map(lambda x: (x[0].rsplit(".", 2)[0], x[1])).reduceByKey(lambda x, y: int(x) + int(y))
filtered_output = prefixes_output.sortBy(lambda x: str(x[0]), True).map(lambda x: (x[0], int(x[1])))
# print(filtered_output.collect())
df = spark.createDataFrame(filtered_output)
# df.show()
df.coalesce(1).write.option("mapreduce.fileoutputcommitter.marksuccessfuljobs","false").csv('output/part4_output')