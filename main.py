from pymongo import MongoClient
import numpy as np
import pymongo
import random
# pip install dnspython

USER = "admin"
PASS = "admin"
CONNECTION_STRING = "mongodb+srv://" + USER + ":" + PASS + "@cluster0.0anzo.mongodb.net/Cogni" #?retryWrites=true&w=majority"
FIELDS = ["gender", "age", "sketchTime", "startTime", "count_path", "count_reset", "count_undo"] # TBD: path, label should be generated.


def get_tests(client):
    tests = client.tests.clock.find()
    dict_arr = []
    for test in tests:
        dict = {}
        for field in FIELDS:
            dict[field] = test[field]
        dict["label"] = random.randint(1, 5)
        dict_arr.append(dict)
    return dict_arr

# clear dataset database
def clear_dataset(client):
    dataset = client.ml.dataset
    for test in dataset.find():
        dataset.delete_one(test)

# load data to dataset
def load_data(client, tests):
    dataset = client.ml.dataset
    for test in tests:
        dataset.insert_one(test)

def get_dataset(client):
    dataset = client.ml.dataset
    i = 0
    for test in dataset:
        arr = [i]
        for feature in test:
            arr.append(feature)

    i += 1



if __name__ == "__main__":
    client = MongoClient(CONNECTION_STRING)
    #clear_dataset(client)

    # load data to dataset
    #data = get_tests(client)   # tests = [{}, {}, {}]
    #load_data(client, data)


    dataset = get_dataset(client)
