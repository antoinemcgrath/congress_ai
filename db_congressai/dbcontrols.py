''' dbcontols for mongo database'''
#from pymongo import MongoClient
import tools
import pymongo 
import re


def getCollection(dbname):
    client = pymongo.MongoClient()             #client.close()
    data_base = getattr(client, dbname)   
    return(data_base)     #data_base.logout()

def unique_check(collObject, unique_check, var):
    found = collObject.find({var: unique_check})
    if found.count() == 1:
        founds = []
        for i in found:
            founds.append(i)
        one_found = founds[0]
        print("DUPLICATE:", var, unique_check, "was found.")
        return (one_found)
    else:
        return(True)

def add_url_sources(collObject, unique_check, entry):
    found = collObject.find({'Sha256_1024chunk': unique_check}).count()
    if found == 0:
        collObject.insert(entry)
    else:
        print("DUPLICATE Sha256_1024chunk was found in DB collection", found)
        return (False)



def add_URL(collObject, unique_check, entry):
    found = collObject.find({'URL_Base': unique_check}).count()
    if found == 0:
        collObject.insert(entry)
    else:
        print("DUPLICATE URL_Base was found in DB collection", found)
        return (False)


def pushURL(data_base, Sha256_1024chunk, line):
    #Connect to DB and collection
    collection = "urls"
    urlsObject = getattr(data_base, collection)
    #URL_Wayback_New = "https://web.archive.org/save/" + URL_Base
    Date_Added = tools.current_unix_time()
    URL_Base = re.sub('.*archive.org\/web\/\d*/', '', line)
    #URL_Wayback_First = "https://web.archive.org/web/0/" + URL_Base
    #URL_Wayback_Latest = "https://web.archive.org/web/" + URL_Base
    item4db = { "Date_Added": Date_Added,
                #"URL_Original": line,
                "URL_Base": URL_Base,
                #"URL_Wayback_first": URL_Wayback_First,
                #"URL_Wayback_Latest": URL_Wayback_Latest
                #"URL_Wayback_New": URL_Wayback_New
                "Source_Sha256_1024chunk": Sha256_1024chunk
    }

    add_URL(urlsObject, item4db['URL_Base'], item4db)

def update_byte(data_base, Sha256_1024chunk, Reading_Byte):
    #Connect to DB and collection
    collection = "url_sources"
    url_sourcesObject = getattr(data_base, collection)
    
    unique_check = url_sourcesObject.update_one({
    "Sha256_1024chunk": Sha256_1024chunk
    },{
        '$set': {
            'Reading_Byte': Reading_Byte
            }}, upsert=False)
    