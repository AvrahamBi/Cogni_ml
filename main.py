import random
import pymongo
import numpy as np
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.feature_selection import SelectKBest, chi2
# pip install dnspython

USER = "admin"
PASS = "admin"
CONNECTION_STRING = "mongodb+srv://" + USER + ":" + PASS + "@cluster0.0anzo.mongodb.net/Cogni" #?retryWrites=true&w=majority"
FIELDS = ["_id", "gender", "age", "sketchTime", "startTime", "count_path", "count_reset", "count_undo"] # TBD: path, label should be generated.


def get_tests(client):
    tests = client.tests.clock.find()
    dict_arr = []
    for test in tests:
        dict = {}
        for field in FIELDS:
            if (field == "_id"):
                dict[field] = str(test[field])
                continue
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

def get_dataset(client, target_index):
    db = client.ml.dataset.find()
    matrix = []
    i = 0
    for test in db:
        arr = []
        for feature in test:
            arr.append(test[feature])
        i += 1
        matrix.append(arr)
    matrix = np.array(matrix)
    y = matrix[:,target_index]

    # remove _id column
    x = np.delete(matrix, obj=0, axis=1)
    # remove target column from x
    x = np.delete(matrix, obj=8, axis=1)
    #
    oe = OrdinalEncoder()
    oe.fit(x)
    x = oe.transform(x)
    # encode y
    le = LabelEncoder()
    le.fit(y)
    y = le.transform(y)
    return x , y



if __name__ == "__main__":
    client = MongoClient(CONNECTION_STRING)
    #clear_dataset(client)

    # load data to mongoDb
    #data = get_tests(client)   # tests = [{}, {}, {}]
    #load_data(client, data)

    target_index = 8
    x, y = get_dataset(client, target_index)
    selector = SelectKBest(score_func=chi2, k='all')
    selector.fit(x, y)

    print("")
    print("List of features and scores, higher score means higher correlatoin.")
    print("")
    for i, field in zip(range(len(selector.scores_)), FIELDS[1:]):
        print("feature name:", field + ", score:", round(selector.scores_[i], 2))
