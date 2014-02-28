import os
import sys

print os.name
print sys.platform

print os.getcwd()
path= os.getcwd()+'/data'

print os.path.dirname(path)