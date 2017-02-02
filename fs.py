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
    filename, mkPath = getAbs(currPath, filename)
    for file in fileList[currPath]:
        if file.name == filename:
            raise Exception('File name already exists')
    newFile = File(filename, nbytes, mkPath)
    fileList[mkPath].append(newFile)  # appended file object to file list
    for index in range(len(freeList)):
        if nbytes == 0:
            break
        if freeList[index] is None and (nbytes <= SystemSize):
            freeList[index] = filename
            nbytes -= 1
            SystemSize -= 1


def getAbs(currPath, filename):
    absPath = filename.split("/")
    mkPath = currPath
    if (len(absPath) > 1):
        mkPath = filename.rsplit('/', 2)[0]
        filename = filename.rsplit('/', 2)[1]
    return filename, mkPath


def open(filename, mode):  # example: filename is a
    global SystemSize
    global freeList
    global systemName
    global currPath
    fileToOpen = None
    if mode not in ['r', 'w']:
        raise Exception("Invalid Mode.")
    filename, mkPath = getAbs(currPath, filename)
    dirFiles = fileList[mkPath]
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
    if mkPath == "/":
        return mkPath + filename
    return mkPath + '/' + filename

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
    retString = ""
    if file.read is not True:
        raise Exception("Error: No permission to read this file!")
    if nbytes + file.position > file.size:  # trying to read more bytes than size of file
        raise Exception("Error: trying to read more bytes than length of file.")

    for word in file.content[file.position: file.position + nbytes]:
        retString += word
        file.position += 1
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
    filename, mkPath = getAbs(currPath, filename)

    if mkPath not in fileList:
        raise Exception("Path doesn't exist.")

    for file in fileList[mkPath]:
        if file.name == filename:
            if file.open is True:
                raise Exception("File is still open.")
            else:
                fileIndex = fileList[mkPath].index(file)
                del fileList[mkPath][fileIndex]
                del file
                break


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
    doesDirExist(dirname,False)
    absPath = dirname.split("/")
    if( len(absPath) > 1):
        mkPath = dirname
    else:
        mkPath = currPath + dirname + "/"
    fileList[mkPath] = []


def chdir(dirname):
    global SystemSize
    global freeList
    global systemName
    global currPath
    if dirname == '..':
        absPath = currPath.split("/")
        currPath = '/'.join(absPath[:-2]) + '/'
    else:
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
    create("x", 10)
    open("x", "w")
    write("x", "abcdefg")
    seek("x", 2)
    fd = open("x", "r")
    print read("/x", 3)
    open("x", "w")
    write("x", "XX")
    open("x", "r")
    print read("/x", 3)
    close(fd)
    delfile("x")
    print fileList

def testDirs():
    mkdir("a")
    mkdir("/a/b")
    create("/a/b/file.txt",2)
    fd = open("/a/b/file.txt","r")
    print fileList
    print fd
testFiles()
testDirs()



