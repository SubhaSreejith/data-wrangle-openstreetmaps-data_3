import json

def insert_data(data, db):

    # Your code here. Insert the data into a collection 'bengaluru_india'
    for record in data:
        db.bengaluru_india.insert(record)
    pass


if __name__ == "__main__":
    
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    with open('bengaluru_india.json') as f:
        data = json.loads(f.read())
        insert_data(data, db)
        print db.bengaluru_india.find_one()