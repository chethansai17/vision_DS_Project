import pymongo

if __name__=="__main__":
    print("Welcome to mongo")
    client=pymongo.MongoClient("mongodb://localhost:27017")
    database=client["Project"]
    collection=database["MYProjectTEST"]
    dictionary={"_ID":2,"specific_ID":"1_2","Type":"Circle","Defects":True,"Colour":True,"coordinates":(0,0),"Reaching_Time":4050}

    collection.insert_many(dictionary)

