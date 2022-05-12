from pymongo import MongoClient
import pymongo
#import dnspython

DB_NAME = "Cogni"
USER = "admin"
PASS = "admin"
CONNECTION_STRING = "mongodb+srv://" + USER + ":" + PASS + "@cluster0.0anzo.mongodb.net/Cogni" #?retryWrites=true&w=majority"

FIELDS = ["gender", "age", "sketchTime", "startTime", "count_path", "count_reset", "count_undo"] # TBD: path, label should be generated.


def get_database():
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    clock = client.tests.clock.find({"date":1641314369550})
    for c in clock:
        print(c)





if __name__ == "__main__":
    dbname = get_database()
