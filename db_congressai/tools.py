''' tools '''
import dbcontrols
import sys
import hashlib
import magic #pip3 install python-magic #https://github.com/ahupp/python-magic


def Sha256_1024chunk(a_file):
    # Make a hash object
    h = hashlib.sha256()
    # Open file for reading in binary mode
    with open(a_file,'rb') as file:
        # Loop till the end of the file
        chunk = 0
        chunk = file.read(1024)
        h.update(chunk)
    # Return the hex representation of digest
    print(h.hexdigest())
    return h.hexdigest()

def Sha256_file(a_file):
    # Make a hash object
    h = hashlib.sha256()
    # Open file for reading in binary mode
    with open(a_file,'rb') as file:
        # Loop till the end of the file
        chunk = 0
        # Entire file
        while chunk != b'':
           # Read 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
    # Return the hex representation of digest
    print(h.hexdigest())
    return h.hexdigest()



def current_unix_time():
    import time
    unix_time = time.time()
    return(unix_time)

def unix_to_readable_time(unix_time):
    from datetime import datetime
    readable_time = datetime.fromtimestamp(float(unix_time)).isoformat()
    return(readable_time)

def query_yes_no(question, default=None):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = str('"'+input()+'"').lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def filetype_magic(Filepath):
    Filetype_file = magic.from_file(Filepath)
    #Filetype_buffer = magic.from_buffer(open(Filepath).read(1024))
    Filetype_mime = magic.from_file(Filepath, mime=True)
    return(Filetype_file, Filetype_mime)


def readfile(data_base, item4db, Reading_Byte):
    with open(item4db['Filepath'], "r") as File:
        File.seek(Reading_Byte)
        for line in File:
            print(line)
            Reading_Byte += len(line)
            line = line.rstrip()
            dbcontrols.pushURL(data_base, item4db['Sha256_1024chunk'], line)
            dbcontrols.update_byte(data_base, item4db['Sha256_1024chunk'], Reading_Byte)

