''' dbcontols for mongo database'''
#from pymongo import MongoClient
import pymongo 


def getCollection(dbname, collection):
    client = pymongo.MongoClient()
    data_base = getattr(client, dbname)
    collObject = getattr(data_base, collection)
    return collObject



def add_url_sources(collObject, unique_check, entry):
    found = collObject.find({'Sha256': unique_check}).count()
    if found == 0:
        collObject.insert(entry)
    else:
        print("DUPLICATE URL LIST: Found", found, "matching Sha256 entry in DB:congressai Collection:url_sources found")
        return (False)

'''def add_url_sources(collObject, unique_check, entry):
    bulk = pymongo.bulk.BulkOperationBuilder(collObject, ordered=True)
    bulk.find({ 
        "Sha256": unique_check
        }).upsert().update_one({
        "$setOnInsert": #{
            # Just the "insert" fields or just "data" as an object for all
            entry #}
            ,
        "$set": {
            # Any other fields "if" you want to update on match
        }
    })
    result = bulk.execute()'''