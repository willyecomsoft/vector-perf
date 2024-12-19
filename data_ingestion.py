import pandas as pd
import random
from couchbaseops import insert_doc
import threading
import time
import csv

def load_rgb_data(file_path):
    # Load the JSON data into a pandas DataFrame
    df = pd.read_json(file_path)
    return df

def modify_embedding_vector(embedding_vector): 
    for i in range(0, len(embedding_vector), 2):
        change = random.uniform(0.001, 0.009)
        if random.choice([True, False]):
            embedding_vector[i] += change
        else:
            embedding_vector[i] -= change
    return embedding_vector

def process_row(row, X):
    for _ in range(X):
        row['embedding_vector_dot'] = modify_embedding_vector(row['embedding_vector_dot'])
        
        # get current time in local time format
        start_time = time.localtime()
        insert_doc("vector-sample", "color", "rgb", row.to_dict(), None, False, True)
        
        # print finish time and time difference in milliseconds
        completion_time = time.localtime()
        time_difference = int((time.time() - time.mktime(start_time)) * 1000) # in milliseconds
        
        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', start_time)
        completion_time_str = time.strftime('%Y-%m-%d %H:%M:%S', completion_time)
        
        print(f"Start Time: {start_time_str}, Completion Time: {completion_time_str}, Time Difference: {time_difference} ms")
        with open('dataingestion.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([start_time_str, completion_time_str, time_difference])



THREADS = 10
ITERATION = 100

# Example usage
file_path = 'rgb.json'
rgb_data = load_rgb_data(file_path)


def run_single_thread():    
    for index, row in rgb_data.iterrows():
        for _ in range(ITERATION):
            row['embedding_vector_dot'] = modify_embedding_vector(row['embedding_vector_dot'])
        
            # get current time in local time format
            start_time = time.localtime()
            insert_doc("vector-sample", "color", "data", row.to_dict(), None, False, True)
            
            # print finish time and time difference in milliseconds
            time_difference = int((time.time() - time.mktime(start_time)) * 1000) 
            
            # print(f"Start Time: {start_time_str}, Completion Time: {completion_time_str}, Time Difference: {time_difference} ms")
            with open('dataingestion.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([time_difference])


threads = []

for _ in range(THREADS):
    thread = threading.Thread(target=run_single_thread)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()