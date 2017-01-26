README.TXT

import os

freelist = [None] * 5 # freelist = [A, A, A, None, None]
filelist = []

def init(fsname):
  size = 5 # TODO: get fsname's size
  #nfile = open(fsname) # open the file
  fd = os.open(fsname, 'r')
  
def create(filename, nbytes):
  #tempfile = file.init(filename, nbytes)
  name = filename
  size = nbytes # size of file
  occupied = 0
  content = [None] * size
  #filelist.append(tempfile) # appended file object to file list
    
  # TODO: NOT ENOUGH SPACE???
  spaceneeded = nbytes # file system = 5 bytes, file A needed 3 bytes
  for space in freelist:
      if space is None:
        space = filename
        spaceneeded = spaceneeded - 1
      if spaceneeded == 0:
        break
    
init("abc.txt")
