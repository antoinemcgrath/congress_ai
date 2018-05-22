import dbcontrols #dbcontrols.py
import tools      #tools.py
import sys
import time



# Connect to DB and collection
dbname = "congressai"
collection = "url_sources"
data_base = dbcontrols.getCollection(dbname)
url_sourcesObject = getattr(data_base, collection)

print('\n' + "Thank you for submitting a list of URLs" + '\n')

# Locate file containing URL list
Filepath = input("Drag file here or otherwise specify it's filepath: ")
Filepath = Filepath.replace("\\","")
#Filepath =  '"' + Filepath +'"'
Filename = Filepath.split("/")[-1]

# Check DB to see if Filename exists in DB
unique_check = dbcontrols.unique_check(url_sourcesObject, Filename, "Filename")

# Filename is unique it does not exist in collection, create file metadata
if unique_check == True:
    Sha256_1024chunk = tools.Sha256_1024chunk(Filepath)
    Sha256_file = tools.Sha256_file(Filepath)
    Filetypes = tools.filetype_magic(Filepath)
    Filetype_file, Filetype_mime = Filetypes
    print("Filetype is:", Filetype_file, Filetype_mime)
    Date_Added = tools.current_unix_time()
    Reading_Byte = 0
    Source = input("Enter your source for these urls:")
    Inputer = input("Enter your name:")
    Details = input("If desired enter a note:")
    #File_Lines = sum(1 for line in open(Filepath))


    item4db = { "Filename": Filename,
                "Filepath": Filepath,
                "Sha256_1024chunk": Sha256_1024chunk,
                "Sha256_file": Sha256_file,
                "Filetype_file": Filetype_file,
                "Filetype_mime": Filetype_file,
                "Reading_Byte": Reading_Byte,
                "Date_Added":Date_Added,
                "Source": Source,
                "Inputer": Inputer,
                "Details": Details }
    proceed = dbcontrols.add_url_sources(url_sourcesObject, item4db['Sha256_1024chunk'], item4db)
    if proceed == False:
        print("Previously this file with an identical Sha256 was submitted with a different Filename. Closing")
        sys.exit()


# Filename exists, reuse file metadata
else:
    time.sleep(1)
    print('\n' + str(unique_check) + '\n')
    time.sleep(1)
    question = ("Resume upload of URL list with the above variables?")
    proceed = tools.query_yes_no(question, default=None)
    if proceed == False:
        print("Restart with a unique filename. Closing.")
        sys.exit()
    print("Upload of URLs will resume with existing item variables.")
    item4db = unique_check


## Upload/Continue to upload URLs to URL collection
Reading_Byte = (item4db['Reading_Byte'])
print("Starting/Resuming URL uploads from byte:", Reading_Byte)
tools.readfile(data_base, item4db, Reading_Byte)