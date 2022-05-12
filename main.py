from pymongo import MongoClient
import pymongo
# pip install dnspython

USER = "admin"
PASS = "admin"
CONNECTION_STRING = "mongodb+srv://" + USER + ":" + PASS + "@cluster0.0anzo.mongodb.net/Cogni" #?retryWrites=true&w=majority"
FIELDS = ["gender", "age", "sketchTime", "startTime", "count_path", "count_reset", "count_undo"] # TBD: path, label should be generated.


def get_database():

    client = MongoClient(CONNECTION_STRING)
    tests = client.tests.clock.find()

    for test in tests:
        print()
        print("Test id:", test["_id"])
        for field in FIELDS:
            print(field, test[field])





if __name__ == "__main__":
    dbname = get_database()
