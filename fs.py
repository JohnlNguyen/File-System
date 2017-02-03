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
    for file in fileList[mkPath]:
        if file.name == filename:
            raise Exception('File name already exists')
    newFile = File(filename, nbytes)

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
        mkPath = filename.rsplit('/', 1)[0] + "/"
        filename = filename.rsplit('/', 1)[1]
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
    return mkPath + filename


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


def mkdir(dirname):  # Ex: b
    global SystemSize
    global freeList
    global systemName
    global currPath
    absPath = dirname.split("/")  # absPath = ['b']
    if (len(absPath) > 1):  # nah bro
        mkPath = dirname + "/"
    else:
        mkPath = currPath + dirname + "/"  # mkPath = '/a/c/' + 'b' + '/'
    doesDirExist(mkPath, False)
    fileList[mkPath] = []


def chdir(dirname):  # Ex: dirname = '/a/b'
    global SystemSize
    global freeList
    global systemName
    global currPath
    if dirname == '.':
        return
    if dirname == '..':  # Nope
        absPath = currPath.split("/")
        currPath = '/'.join(absPath[:-2]) + '/'
    else:
        absPath = dirname.split("/")  # absPath = ['', '']
        if (len(absPath) > 1):  # Yes
            if dirname == '/':  # Yes
                chPath = '/'  # Yes
            else:
                chPath = dirname + "/"
        else:
            chPath = currPath + dirname + "/"
        doesDirExist(chPath, True)
        currPath = chPath


def deldir(dirname):  # dirname = '/a/b'
    global SystemSize
    global freeList
    global systemName
    global currPath  # currPath = '/'
    absPath = dirname.split("/")
    if (len(absPath) > 1):
        delPath = dirname + "/"
    else:
        delPath = currPath + dirname + "/"
    doesDirExist(delPath, True)  # doesDirExist('/a/b/', True)
    # delPath = '/a/b/'
    length = len(delPath)  # length = 5
    for key, values in fileList.items():
        if key[:length] == delPath:  # key[:5]
            for val in values:
                if val.open is True:
                    raise Exception("File(s) still open.")
            del fileList[key]
    return


def listdir(dirname):  # '/a/b'
    global SystemSize
    global freeList
    global systemName
    global currPath
    if dirname == '.':
        lsPath = currPath
    elif dirname == '..':
        absPath = currPath.split('/')
        lsPath = '/'.join(absPath[:-2]) + '/'
    else:
        absPath = dirname.split("/")
        if (len(absPath) > 1):
            lsPath = dirname + "/"
        else:
            lsPath = currPath + dirname + "/"
        doesDirExist(lsPath, True)
    alldir = []
    depth = len(lsPath.split('/'))
    for key in fileList.keys():
        if key[:len(lsPath)] == lsPath:
            directory = key.split('/')
            if (len(directory) - 1 == depth):
                alldir.append(directory[-2])
    return alldir


def doesDirExist(dirPath, itShouldBe):  # Ex: dirname = /a/b , itShouldBe = True
    global SystemSize
    global freeList
    global systemName
    global currPath
    if dirPath not in fileList and itShouldBe is True:  # if '/a/b' + 'b' + '/' , False
        raise Exception('Directory does not exist')
    if dirPath in fileList and itShouldBe is False:  # if '/a/c/' + 'b' + '/', False
        raise Exception('Directory already exists')  # raise this exception


def suspend():
    global SystemSize
    global freeList
    global systemName
    global currPath

    for files in fileList.values():
        for file in files:
            if file.open is True:
                raise Exception("File(s) still open, cannot suspend.")
    file = io.open(systemName, 'wb')
    pickle.dump(SystemSize, file)
    pickle.dump(freeList, file)
    pickle.dump(systemName, file)
    pickle.dump(currPath, file)
    file.close


def resume():
    global SystemSize
    global freeList
    global systemName
    global currPath

    file = io.open(systemName, 'r')
    systemSize = pickle.load(file)
    freeList = pickle.load(file)
    systemName = pickle.load(file)
    currPath = pickle.load(file)


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
    init("abc.txt")
    mkdir("a")
    mkdir("/a/b")
    mkdir("/a/c")
    mkdir("/a/d")
    mkdir("/a/b/k/d")
    mkdir("/a/b/f")
    create("/a/b/file.txt", 2)
    fd = open("/a/b/file.txt", "r")
    close(fd)
    chdir("/a/b")
    print fileList
    print currPath
    print listdir(".")
    print listdir("/a/b/k")


# testFiles()
testDirs()
# getAbs('')
