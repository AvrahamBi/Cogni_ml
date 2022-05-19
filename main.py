import random
import pymongo
import operator
import string
import numpy as np
#import pyplot
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.feature_selection import SelectKBest, chi2
# pip install dnspython

USER = "admin"
PASS = "admin"
CONNECTION_STRING = "mongodb+srv://" + USER + ":" + PASS + "@cluster0.0anzo.mongodb.net/Cogni" #?retryWrites=true&w=majority"
FIELDS = ["_id", "gender", "age", "sketchTime", "startTime", "count_path", "count_reset", "count_undo"] # TBD: path, label should be generated.
TARGET_INDEX = 8
GENERATE_TESTS = 50



def generate_test():
    _id = ''.join(random.choice(string.ascii_letters) for i in range(8))
    gender = random.randint(0, 1)
    age = random.randint(8, 90)
    sketchTime = random.randint(100, 100000)
    startTime = random.randint(100, 100000)
    count_path = random.randint(4, 24)
    count_reset = random.randint(0, 3)
    count_undo = random.randint(0, 6)
    label = random.randint(1, 5)
    return {'id' : _id, 'gender' : gender, 'age' : age, 'sketchTime' : sketchTime, 'startTime' : startTime,
            'count_path' : count_path, 'count_reset' : count_reset, 'count_undo' : count_undo, 'label' : label}

def get_tests(client):
    tests = client.tests.clock.find()
    tests_arr = []
    for test in tests:
        dict = {}
        for field in FIELDS:
            if (field == "_id"):
                dict[field] = str(test[field])
                continue
            dict[field] = test[field]
        dict["label"] = random.randint(1, 5)
        tests_arr.append(dict)
    if (0 < GENERATE_TESTS):
        for i in range(GENERATE_TESTS):
            #tests_arr.append(generate_test())
            pass
    print("Tests loaded from MongoDb and", GENERATE_TESTS, "tests have been generated")
    return tests_arr

# clear dataset database
def clear_dataset(client):
    dataset = client.ml.dataset
    for test in dataset.find():
        dataset.delete_one(test)
    print("MongoDb dataset has been deleted!")

# load data to dataset
def load_data(client, tests):
    dataset = client.ml.dataset
    for test in tests:
        dataset.insert_one(test)
    print("Dataset has been uplpaded to MongoDb")

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

def get_scores(client, target_index):
    x, y = get_dataset(client, target_index)
    selector = SelectKBest(score_func=chi2, k='all')
    selector.fit(x, y)
    scores_dict = {}
    for i, field in zip(range(len(selector.scores_)), FIELDS[1:]):
        scores_dict[field] = round(selector.scores_[i], 2)
    sorted_scores_dict = {k: v for k, v in sorted(scores_dict.items(), reverse=True, key=lambda item: item[1])}
    return scores_dict, sorted_scores_dict

def show_scores(sorted_scores_dict):
    print("")
    print("List of features and scores")
    print("higher score means higher correlation between feature to target.")
    for key in sorted_scores_dict:
        #print(key,'\t', sorted_scores_dict[key])
        line = '%14s %14s' % (key, sorted_scores_dict[key])
        print(line)

if __name__ == "__main__":
    client = MongoClient(CONNECTION_STRING)

    # clear MongoDb dataset
    clear_dataset(client)

    # get tests from MongoDb and create dataset
    data = get_tests(client)   # tests = [{}, {}, {}]

    # upload dataset into MongDb
    load_data(client, data)

    # get scores of features
    scores_dict, sorted_scores_dict = get_scores(client, TARGET_INDEX)

    # show scores
    show_scores(sorted_scores_dict)


