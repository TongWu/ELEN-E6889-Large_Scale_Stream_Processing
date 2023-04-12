"""
Part 3
Extend the application to compute the total number of bytes served per time window of 1 hour, (with tumbling windows)
for each unique IP

csv file that includes results for interval 30:00:00:00 to 30:00:59:59  with:
IP, Bytes
Sort by IP in string ascending order so 100.1.2.3 comes before 99.2.3.5.
"""

from pyspark import SparkContext
import ipaddress
from pyspark.sql import SparkSession
sc = SparkContext()
spark = SparkSession(sc)

# Determine whether the input is an IP address but not a domain
def is_ip_address(addr):
    try:
        ip = ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

# Extract domain&IP, time, bytes
output = sc.textFile("epa-http.txt").map(lambda x: (
x.replace(':', ' ').split(' ')[0], x.replace(':', ' ').split(' ')[1].replace('[', ''), x.replace(':', ' ').split(' ')[2],
x.replace(':', ' ').split(' ')[len(x.replace(':', ' ').split(' ')) - 1])).filter(lambda x: x[3] != '-')
# Filter out domain name
filtered_output = output.filter(lambda x: is_ip_address(str(x[0]))).map(lambda x: (x[0], int(x[1]), int(x[2]), int(x[3])))
# Start tumbling windows
print("29H:23H")
hourly_output = filtered_output.filter(lambda x: x[1] == 29 and x[2] == 23).map(lambda x: (x[0], x[3])).reduceByKey(lambda x, y: int(x) + int(y))
print(hourly_output.collect())
print('\n')
for i in range(24):
    print("30D:"+str(i)+"H")
    hourly_output = filtered_output.filter(lambda x: x[1] == 30 and x[2] == i).map(lambda x: (x[0], x[3])).reduceByKey(lambda x, y: int(x) + int(y))
    print(hourly_output.collect())
    print('\n')
# Output results for interval 30:00:00:00 to 30:00:59:59 to csv file
hourly_output = filtered_output.filter(lambda x: x[1] == 30 and x[2] == 0).map(lambda x: (x[0], x[3])).reduceByKey(lambda x, y: int(x) + int(y))
# hourly_output.take(10)
filtered_output = hourly_output.sortBy(lambda x: str(x[0]), True).map(lambda x: (x[0], int(x[1])))
# print(filtered_output.collect())
# filtered_output.toDF().show()
df = spark.createDataFrame(filtered_output)
# df.show()
df.coalesce(1).write.option("mapreduce.fileoutputcommitter.marksuccessfuljobs","false").csv('output/part3_output')