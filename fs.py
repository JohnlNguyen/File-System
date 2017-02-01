# README.TXT


import io
import os
import pickle
from file import File

SystemSize = 0
freeList = []
fileList = {}
currPath = ""
systemName = ""


def init(fsname):
    global SystemSize
    global freeList
    global systemName
    global currPath
    systemName = fsname
    SystemSize = os.path.getsize(fsname)
    freeList = [None] * SystemSize
    fileList['/'] = []
    currPath = "/"


def create(filename, nbytes):
    global SystemSize
    global freeList
    global systemName
    global currPath
    if (nbytes > SystemSize):
        raise Exception('No More Space')

    for file in fileList[currPath]:
        if file == filename:
            raise Exception('File name already exists')

    newFile = File(filename, nbytes, currPath)

    fileList[currPath].append(newFile)  # appended file object to file list
    for pos in range(len(freeList)):
        if nbytes == 0:
            break
        if freeList[pos] is None and (nbytes <= SystemSize):
            freeList[pos] = filename
            nbytes -= 1
            SystemSize -= 1

def open(filename, mode):  # example: filename is a
    global SystemSize
    global freeList
    global systemName
    global currPath
    dirFiles = fileList[currPath]
    fileToOpen = None
    if mode not in ['r', 'w']:
        raise Exception("Invalid Mode.")

    for file in dirFiles:
        if filename == file.name:
            fileToOpen = file
            break
    if fileToOpen is None:
        raise Exception("File does not exist.")
    fileToOpen.open = True
    if mode == "r":
        fileToOpen.read = True
    if mode == "w":
        fileToOpen.read = False
    if currPath == "/":
        return currPath + filename
    return currPath + '/' + filename


def close(fd):
    global SystemSize
    global freeList
    global systemName
    global currPath
    fileToClose = isFD(fd)
    fileToClose.open = False
    fileToClose.read = False
    fileToClose.write = False


def write(fd, writebuf):
    global SystemSize
    global freeList
    global systemName
    global currPath
    F = isFD(fd)
    if (F.size - F.occupied) < len(writebuf):
        raise Exception("File not big enough")
    if F.read is True:
        raise Exception("File is read-only")
    if F.open is False:
        raise Exception("File is not open")
    F.writeToFile(writebuf)


def read(fd, nbytes):
    global SystemSize
    global freeList
    global systemName
    global currPath
    file = isFD(fd)
    bytesToRead = nbytes
    retString = ""
    if file.read is not True:
        raise Exception("Error: No permission to read this file!")
    if nbytes > file.size:  # trying to read more bytes than size of file
        raise Exception("Error: trying to read more bytes than length of file.")
    if nbytes + file.position > file.size:  # trying to read more bytes than size of file
        raise Exception("Error: trying to read more bytes than length of file.")

    for word in file.content:
        retString += word
        bytesToRead -= 1
        file.position += 1
        if bytesToRead == 0:
            break

    return retString


def readlines(fd):
    global SystemSize
    global freeList
    global systemName
    global currPath
    currLine = ""
    fileLines = []
    file = isFD(fd)

    if file.read is not True:
        raise Exception("Error: No permission to read this file!")
    for byte in file.content:
        currLine += byte
        if byte == "\n":
            fileLines.append(currLine)
            currLine = ""
    if currLine != "":
        fileLines.append(currLine)
    return fileLines

def length(fd):
    global SystemSize
    global freeList
    global systemName
    global currPath
    file = isFD(fd)
    return file.occupied

def isFD(fd):
    global SystemSize
    global freeList
    global systemName
    global currPath
    # sample fd: /dir1/dir2/hi.txt
    # need to find out if fd exists
    # fileList: '/dir1/dir2': [hi.txt, bye.txt]
    # Example: fd = /a/b/abc.txt
    dirsp = fd.split('/')  # Example: dirsp = ['a', 'b', 'abc.txt']
    filename = dirsp[-1]  # Example: filename = 'abc.txt'
    dirPath = '/'.join(dirsp[:-1]) + '/'  # Example: dirpath = /a/b/

    if dirPath not in fileList:
        raise Exception("No such file descriptor.")
    dirFiles = fileList[dirPath]
    for file in dirFiles:
        if filename == file.name:
            return file
    raise Exception("No such file descriptor.")


def pos(fd):
    global SystemSize
    global freeList
    global systemName
    global currPath
    file = isFD(fd)
    return file.position


def seek(fd, pos):
    global SystemSize
    global freeList
    global systemName
    global currPath
    file = isFD(fd)
    if pos < 0 or pos > file.size or pos > file.occupied:
        raise Exception("Incorrect position")
    file.position = pos
    return


def delfile(filename):
    global SystemSize
    global freeList
    global systemName
    global currPath
    pathToFile = currPath + filename
    if pathToFile not in fileList:
        raise Exception("File doesn't exist.")
    if fileList[pathToFile].open is True:
        raise Exception("File is still open.")
    fileToDelete = fileList[pathToFile]
    del fileList[pathToFile]
    del fileToDelete


def isdir(dirname):
    global SystemSize
    global freeList
    global systemName
    global currPath
    if currPath + dirname + "/" in fileList:
        return True
    return False


def mkdir(dirname):
    global SystemSize
    global freeList
    global systemName
    global currPath
    doesDirExist(dirname, False)
    mkPath = currPath + dirname + "/"
    fileList[mkPath] = []


def chdir(dirname):
    global SystemSize
    global freeList
    global systemName
    global currPath
    doesDirExist(dirname, True)
    currPath = currPath + dirname + '/'


def deldir(dirname):
    global SystemSize
    global freeList
    global systemName
    global currPath
    doesDirExist(dirname, True)

    pathToDir = currPath + dirname + '/'
    length = len(pathToDir)

    for key, values in fileList.items():
        if key[:length] == pathToDir:
            for val in values:
                if val.open is True:
                    raise Exception("File(s) still open.")
            del fileList[key]
    return


def listdir():
    global SystemSize
    global freeList
    global systemName
    global currPath
    # in /a/b/
    # /a/b/ has dir c, d, e
    # keys are /a/b/c/, /a/b/d/, /a/b/e/
    alldir = []
    for key in fileList.keys():
        if key[:len(currPath)] == currPath:
            directory = key.split('/')
            alldir.append(directory[-2])
    return alldir


def doesDirExist(dirname, itShouldBe):
    global SystemSize
    global freeList
    global systemName
    global currPath
    if currPath + dirname + "/" not in fileList and itShouldBe is True:
        raise Exception('Directory does not exist')
    if currPath + dirname + "/" in fileList and itShouldBe is False:
        raise Exception('Directory already exists')


def testFiles():
    init("abc.txt")
    create("x", 7)
    create("y", 7)
    open("x", "w")
    open("y", "w")
    write("/x", "b\na\n")
    write("/y", "test")
    open("x", "r")
    open("y", "r")
    print "pos %d" % pos("/y")
    #print "read " + read("/x", 2)
    #print readlines("/x")
    #close("/x")
    #print "pos %d" % pos("/x")
    """seek("/x", 4)
    print "length %d" % length("/x")
    mkdir("a")
    print dirMap
    print currPath"""
testFiles()
