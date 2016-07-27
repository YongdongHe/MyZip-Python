#coding=utf8
#from MyZipUtils import *
import struct
print ord('t')
a = ""
f = open('testdata.txt','w')
f.write(struct.pack('b',116))
f.flush()
f.close()