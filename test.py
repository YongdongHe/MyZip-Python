from MyZipUtils import *
import struct
print ord('t')
a = "hello"
output = open('test', 'wb')
ot = [1,2]
o = struct.pack('b',-127)
output.write(o)
output.flush()
output.close()
a = [1,2]
b = a
b[0] = 3
l = [2,3,4]
print l.pop(0)
print l