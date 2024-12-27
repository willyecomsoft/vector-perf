import threading
import time
import os
from dotenv import load_dotenv
from couchbaseops import cluster, cb_vector_search
import random 
from sample_vector import VECTOR
import csv
from datetime import timedelta
from sharedfunctions.print import print_success

load_dotenv()

QUERY_USER_COUNT = os.getenv("QUERY_USER_COUNT", 12)
QUERY_VECTOR_COUNT = os.getenv("QUERY_VECTOR_COUNT", 1)

now_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
file_name = f"{QUERY_USER_COUNT}*{QUERY_VECTOR_COUNT}_{now_str}.csv"

RAMDOM_START = os.getenv("RAMDOM_START", 0.001)
RAMDOM_END = os.getenv("RAMDOM_END", 0.05)

def modify_embedding_vector(embedding_vector): 
    copy = embedding_vector[:]
    for i in range(0, len(copy), 2):
        if random.choice([True, False]):
            copy[i] *= -1
        change = random.uniform(float(RAMDOM_START), float(RAMDOM_END))
        copy[i] += change
    return copy


def sleep_until_next_second():
    current_time = time.time()
    sleep_duration = 1 - (current_time - int(current_time))
    time.sleep(sleep_duration)
    
    
def query_couchbase():
    while True:
        vectors = []
        
        for _ in range(int(QUERY_VECTOR_COUNT)):
            vector = modify_embedding_vector(VECTOR)
            vectors.append(modify_embedding_vector(VECTOR))

        # get current time in local time format
        start_time = time.time()
        print(f"Start Time: {time.strftime('%X', time.localtime(start_time))}")

        color = ""
        count = 0

        for vector in vectors:
            result = cb_vector_search("vector-sample", "color", "color-vector", "embedding_vector_dot", vector, ["color"])  
            
            for row in result.rows():
                color = row.fields.get("color")  # 提取指定欄位
                count += 1

        # print finish time and time difference in milliseconds
        completion_time = time.time()
        time_difference = completion_time - start_time
        
        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
        completion_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(completion_time))
        # append start_time, completion_time, and time_difference the a new line in results.csv
        
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([count, int(time_difference * 1000.0), f'{time_difference} sec', start_time_str, completion_time_str, color, threading.get_ident()])

        sleep_until_next_second()


threads = []
for _ in range(int(QUERY_USER_COUNT)):
    thread = threading.Thread(target=query_couchbase)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
