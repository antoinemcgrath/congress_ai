import dbcontrols
import tools
import sys

proceed = tools.query_yes_no("Do you have urls for download?")

if proceed == False:
    print("Closing")
    sys.exit()

print("Continuing")


dbname = "congressai"
collection = "url_sources"
collObject = dbcontrols.getCollection(dbname, collection)


Filepath = input("Drop in or type your file:")
Sha256 = tools.sha256_file(Filepath)
#If Sha256 == existing Sha256
#   print("This file has already been contributed")
#   exit

Filetype = tools.filetype_magic(Filepath)
print("Filetype is:", Filetype)

Date_Added = tools.current_unix_time()
Source = input("Enter your source for these urls:")
Inputer = input("Enter your name:")
Details = input("If desired enter a note:")

item4db = { "Filepath": Filepath,
            "Sha256": Sha256,  
            "Filetype": Filetype,             
            "Date_Added":Date_Added,   
            "Source": Source, 
            "Inputer": Inputer,  
            "Details": Details }

proceed = dbcontrols.add_url_sources(collObject, item4db['Sha256'], item4db)

if proceed == False:
    print("Closing")
    sys.exit()

print (proceed)


print("Item for DB's " + str(len(item4db))
     + " values are:", item4db)
