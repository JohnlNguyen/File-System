# README.TXT

import os

freelist = [None] * 5 # freelist = [A, A, A, None, None]
filelist = []
fd = None

def init(fsname):
  size = 5 # TODO: get fsname's size
  #nfile = open(fsname) # open the file
  fd = open(fsname)
  
def create(filename, nbytes):
  tempfile = file(filename, nbytes)
  name = filename
  size = nbytes # size of file
  occupied = 0
  content = [None] * size
  filelist.append(tempfile) # appended file object to file list
  # TODO: NOT ENOUGH SPACE???
  spaceneeded = nbytes # file system = 5 bytes, file A needed 3 bytes
  for pos in range(0, len(freelist)):
    if freelist[pos] is None:
      freelist[pos] = filename
      spaceneeded = spaceneeded - 1
    if spaceneeded == 0:
      break
  
class file:
  def __init__(self, filename, nbytes):
    self.name = filename
    self.size = nbytes # size of file
    self.occupied = 0
    self.content = [None] * self.size


'''
>>> import fs
>>> fs.init("abc.txt")
>>> fs.create("x", 2)
>>> fs.freelist
['x', 'x', None, None, None]
>>> fs.create("y", 1)
>>> fs.freelist
['x', 'x', 'y', None, None]
'''