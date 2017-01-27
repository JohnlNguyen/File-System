# README.TXT


import os
SystemSize = 0
freeList = []
fileList = []

def init(fsname):
    fd = open(fsname, "w")
    fd.write("a" * 5) #Change 5 to be what we want the size of the system to be
    fd.close()
    pwd = os.getcwd() + "/" + str(fsname)
    global SystemSize
    global freeList
    SystemSize = os.path.getsize(pwd)
    freeList = [None] * SystemSize

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