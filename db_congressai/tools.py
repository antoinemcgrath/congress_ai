''' tools '''

def sha256_file(a_file):
    import sys
    import hashlib
    # Make a hash object
    h = hashlib.sha256()
    # Open file for reading in binary mode
    with open(a_file,'rb') as file:
        # Loop till the end of the file
        chunk = 0
        while chunk != b'':
           # Read 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
    # Return the hex representation of digest
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
    import sys
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
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def filetype_magic(Filepath):
    import magic #pip3 install python-magic #https://github.com/ahupp/python-magic
    Filetype = magic.from_file(Filepath)
    return(Filetype)