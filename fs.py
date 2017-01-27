# README.TXT


import io
import os
from file import File

SystemSize = 0
freeList = []
fileList = {}
currPath = ""
systemName = ""


def init(fsname):
    fd = io.open(fsname, 'wb')
    fd.write("a" * 5)  # Change 5 to be what we want the size of the system to be
    fd.close()
    pwd = os.getcwd() + "/" + str(fsname)
    global SystemSize
    global freeList
    global systemName
    systemName = fsname
    SystemSize = os.path.getsize(pwd)
    freeList = [None] * SystemSize


def create(filename, nbytes):
    path = currPath + "/" + str(filename)
    newFile = File(filename, nbytes, path)
    fileList[path] = newFile  # appended file object to file lisMe
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


def open(filename, mode):  # example: filename is a
    pathToFile = currPath + "/" + filename
    if pathToFile not in fileList:
        raise Exception("File does not exist.")
    if mode not in ['r', 'w']:
        raise Exception("Invalid Mode.")
    fileToOpen = fileList[pathToFile]  # assign File object at pathToFile
    fileToOpen.open = True
    if mode == "r":
        fileToOpen.read = True
    if mode == "w":
        fileToOpen.write = True
    return pathToFile


def close(fd):
    global SystemSize
    global freeList
    if fd not in fileList:
        raise Exception("No such file descriptor.")
    fileToClose = fileList[fd]
    fileToClose.open = False
    fileToClose.read = False
    fileToClose.write = False

def write(fd, writebuf):
    global SystemSize
    global freeList
    if fd not in fileList:
        raise Exception("No such file descriptor.")
    F = fileList[fd]
    if (F.size - F.occupied) < len(writebuf):
        raise Exception("File not big enough")
    if F.read is True:
        raise Exception("File is read-only")
    if F.open is False:
        raise Exception("File is not open")
    F.writeToFile(writebuf)
    f = io.open(systemName, "wb")
    f.write(writebuf)
    f.close()


def read(fd, nbytes):
    global SystemSize
    global freeList
    if fd not in fileList:
        raise Exception("No such file descriptor.")
    file = fileList[fd]  # assign File object at pathToFile
    bytesToRead = nbytes
    tempString = ""
    if file.read is not True:
        raise Exception("Error: No permission to read this file!")
    if nbytes > file.size:  # trying to read more bytes than size of file
        raise Exception("Error: trying to read more bytes than length of file.")

    for word in file.content:
        tempString += word
        bytesToRead -= 1
        file.position += 1
        if bytesToRead == 0:
            break

    return tempString


init("abc.txt")
create("x", 3)
create("y", 1)
open("x", "w")
write("/x", "r")
open("x", "r")
close("/x")