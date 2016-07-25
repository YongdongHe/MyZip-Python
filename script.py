#coding=utf8
from MyZipUtils import *
str1 = """00010101 11001010 11010001 00001101 10000000 00100000 00001100 01000101
11010001 01010101 11011110 00000000 11000110 00011101 00011100 10100101
11001010 00110011 00010000 01001011 01001001 01101000 11010101 10110000
10111101 11111000 01110001 01111111 01101110 11001110 11100110 10101000
10110100 00101000 11001101 10011000 00100000 01111011 01111011 10111000
01000100 01100110 00100111 01100100 01010110 11000101 00000110 10101110
01100010 11001001 11010001 01001110 10111100 10100101 01010011 11101001
00001110 00011111 00011110 10101100 11110011 11111101 00010010 10010001
11000101 01110000"""
s = ""
for item in str.split(str1):
	s += item[::-1]
print s
Header = s[0:1] + s[2] + s[1]
HLIT = s[3:8][::-1]
HDIST = s[8:13][::-1]
HCLEN = s[13:17][::-1]
print "Header: %s"%Header
print "HLIT: %s"%HLIT
print "HDIST: %s"%HDIST
print "HCLEN: %s"%HCLEN
file_data_offset = 17
NUM_OF_CCL = valueOf(HCLEN) + 4
CCLbits = s[file_data_offset : file_data_offset + NUM_OF_CCL * 3]

CCL = printCCL(CCLbits,NUM_OF_CCL)
print CCL

CCL = replaceCCL(CCL)
print "Current CCL:"
print CCL

print "CCL huffman hash map:"
huffman_map3 = getMapOfCCL(CCL)
print huffman_map3
for code in huffman_map3.keys():
	print "%s -> %d"%(code,huffman_map3[code])

cl1_offset = file_data_offset  + NUM_OF_CCL * 3
NUM_OF_CL1 = valueOf(HLIT) + 257
cl1_count = 0
#从偏移处开始搜索
index = cl1_offset
buff = ""
CL1 = []
while cl1_count < NUM_OF_CL1:
	buff += s[index]
	index += 1
	#看当前有没有对应的huffman_map3中的项
	if huffman_map3.has_key(buff):
	 	cl1_value = huffman_map3[buff]
	 	print cl1_value,
	 	if cl1_value == 16:
	 		flag_16 = s[index:index+2]
	 		print flag_16,
	 		index += 2
	 		repeat_value = CL1[-1]
	 		repeat_times = ( 3 + valueOf(flag_16[::-1]))
	 		CL1 += [repeat_value] *  repeat_times
	 		cl1_count += repeat_times
	 	elif cl1_value == 17:
	 		flag_17 = s[index:index+3]
	 		print flag_17,
	 		index += 3
	 		repeat_value = 0
	 		repeat_times = ( 3 + valueOf(flag_17[::-1]))
	 		CL1 += [repeat_value] * repeat_times
	 		cl1_count += repeat_times
	 	elif cl1_value == 18:
	 		flag_18 = s[index:index+7]
	 		print flag_18,
	 		index += 7
	 		repeat_value = 0
	 		repeat_times = ( 11 + valueOf(flag_18[::-1]))
	 		CL1 += [repeat_value] * repeat_times
	 		cl1_count += repeat_times
	 	else:
	 		CL1.append(cl1_value)
	 		cl1_count += 1
	 	buff = ""
print "CL1:"
print CL1
print len(CL1)
