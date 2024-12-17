import threading
import time
from couchbaseops import cluster, cb_vector_search
import random 
from sample_vector import VECTOR
import csv
from datetime import timedelta
from sharedfunctions.print import print_success


cluster.wait_until_ready(timedelta(seconds=5))
print_success("Couchbase setup complete")


def modify_embedding_vector(embedding_vector): 
    for i in range(0, len(embedding_vector), 2):
        change = random.uniform(0.001, 0.009)
        if random.choice([True, False]):
            embedding_vector[i] += change
        else:
            embedding_vector[i] -= change
    return embedding_vector


def sleep_until_next_second():
    current_time = time.time()
    sleep_duration = 1 - (current_time - int(current_time))
    time.sleep(sleep_duration)
    
    
def query_couchbase():
    while True:
        vector = modify_embedding_vector(VECTOR)
        
        # get current time in local time format
        start_time = time.localtime()
        print(f"Start Time: {time.strftime('%X', start_time)}")
        
        result = cb_vector_search("vector-sample", "color", "color-vector", "embedding_vector_dot", vector, ["color"])  
        
        # print finish time and time difference in milliseconds
        completion_time = time.localtime()
        time_difference = time.time() - time.mktime(start_time)
        
        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', start_time)
        completion_time_str = time.strftime('%Y-%m-%d %H:%M:%S', completion_time)
        # append start_time, completion_time, and time_difference the a new line in results.csv
        
        count = 0 
        for _ in result:
            count += 1
        
        with open('res1500k.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([count, start_time_str, completion_time_str, time_difference])
    
        sleep_until_next_second()

    
threads = []
for _ in range(12):
    thread = threading.Thread(target=query_couchbase)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
