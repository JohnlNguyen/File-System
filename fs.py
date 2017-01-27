# README.TXT


import os
SystemSize = 5
freeList = [None]*SystemSize  # freelist = [A, A, A, None, None]
fileList = []
fd = None



def init(fsname):
    fd = open(fsname, "w")
    fd.write("\0" * 5)
    pwd = os.getcwd() + "/" + str(fsname)
    size = os.path.getsize(pwd)
    print size


def create(filename, nbytes):
    new = File(filename, nbytes)
    fileList.append(new)  # appended file object to file list
    global SystemSize
    if (nbytes > SystemSize):
        raise Exception('No More Space')
    for pos in range(len(freeList)):
        if nbytes == 0:
            break
        if freeList[pos] is None and (nbytes <= SystemSize):
            freeList[pos] = filename
            nbytes -= 1
            SystemSize -= 1



class File:
    def __init__(self, filename, size):
        self.name = filename
        self.size = size  # size of file
        self.occupied = 0
        self.content = [None] * self.size

init("abc.txt")
create("x",3)
create("y",1)
print freeList