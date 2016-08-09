#coding=utf8
from MyZipUtils import *
from MyZipData import *
from DeflateData import *
# from EnglishData import *
# from ZhihuZuidaData import *
# from ZhihuFastData import *
# from ZhihuBiaozhunData import *
# from ZhihuJixianData import *
# from yybData import *
import sys
s = ""
for item in str.split(TEST_DATA):
	s += item[::-1]
print s
s = s[:TEST_DATA_SIZE*8]
print len(s)
Header = s[0] + s[2] + s[1]
HLIT = s[3:8][::-1]
HDIST = s[8:13][::-1]
HCLEN = s[13:17][::-1]
huffman_tree_outputfile = open("huffman_tree" + CONFIG_OUTPUT_FILENAME  , 'w')
print "Header: %s"%Header
print "HLIT: %s"%HLIT
print "HDIST: %s"%HDIST
print "HCLEN: %s"%HCLEN
file_data_offset = 17
print '\n\n\n***************CLL'
NUM_OF_CCL = valueOf(HCLEN) + 4
print "num of ccl: %d"%NUM_OF_CCL
CCLbits = s[file_data_offset : file_data_offset + NUM_OF_CCL * 3]

CCL = printCCL(CCLbits,NUM_OF_CCL)
print CCL

CCL = replaceCCL(CCL)
print "Current CCL:"
print CCL
#输出CLL到文件
huffman_tree_outputfile.write("CCL\n")
huffman_tree_outputfile.write(str(CCL))
huffman_tree_outputfile.write("\n")
print "CCL huffman hash map:"
huffman_map3 = getMapOfCCL(CCL)
print huffman_map3
for code in huffman_map3.keys():
	print "%s -> %d"%(code,huffman_map3[code])

print '\n\n\n***************CL1'
cl1_offset = file_data_offset  + NUM_OF_CCL * 3
NUM_OF_CL1 = valueOf(HLIT) + 257
print "num of cl1: %d"%NUM_OF_CL1 
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
	 	print "%s(%d)"%(buff,cl1_value),
	 	if cl1_value == 16:
	 		flag_16 = s[index:index+2]
	 		print flag_16,
	 		index += 2
	 		repeat_value = CL1[-1]
	 		repeat_times = ( 3 + valueOf(flag_16[::-1]))
	 		CL1 += [repeat_value] *  repeat_times
	 		print '%d 个 %d'%(repeat_times,repeat_value)
	 		cl1_count += repeat_times
	 	elif cl1_value == 17:
	 		flag_17 = s[index:index+3]
	 		print flag_17,
	 		index += 3
	 		repeat_value = 0
	 		repeat_times = ( 3 + valueOf(flag_17[::-1]))
	 		CL1 += [repeat_value] * repeat_times
	 		print '%d 个 %d'%(repeat_times,repeat_value)
	 		cl1_count += repeat_times
	 	elif cl1_value == 18:
	 		flag_18 = s[index:index+7]
	 		print flag_18,
	 		index += 7
	 		repeat_value = 0
	 		repeat_times = ( 11 + valueOf(flag_18[::-1]))
	 		CL1 += [repeat_value] * repeat_times
	 		print '%d 个 %d'%(repeat_times,repeat_value)
	 		cl1_count += repeat_times
	 	else:
	 		CL1.append(cl1_value)
	 		cl1_count += 1 
	 	buff = ""
print s[index:]
print "\nCL1:"
print CL1
huffman_tree_outputfile.write("CL1\n")
huffman_tree_outputfile.write(str(CL1))
huffman_tree_outputfile.write("\n")
print len(CL1)
print "CL1 huffman hash map:(length and literal)"
huffman_map1 = getMapOfCL1(CL1)
# print huffman_map1
# for code in huffman_map1.keys():
# 	if huffman_map1[code] < 256:
# 		print "%s -> %c"%(code,chr(huffman_map1[code]))
# 	else:
# 		print "%s -> %d"%(code,huffman_map1[code])
huffman_map1_output = open('huffman_map1.txt', 'w')		
for code in huffman_map1.keys():
	if huffman_map1[code] < 256:
		#huffman_map1_output.write(" %s -> %c \n"%(code,chr(huffman_map1[code])))
		huffman_map1_output.write(" %s -> %s \n"%(code,chr(huffman_map1[code])))
	else:
		huffman_map1_output.write(" %s -> %d \n"%(code,huffman_map1[code]))	
huffman_map1_output.flush()
huffman_map1_output.close()

print '\n\n\n***************CL2'
cl2_offset = index
NUM_OF_CL2 = valueOf(HDIST) + 1
print "num of cl2: %d"%NUM_OF_CL2

cl2_count = 0
index = cl2_offset
buff = ""
CL2 = []

while cl2_count < NUM_OF_CL2:
	buff += s[index]
	index += 1
	#看当前有没有对应的huffman_map3中的项
	if huffman_map3.has_key(buff):
		cl2_value = huffman_map3[buff]
		print cl2_value,
		if cl2_value == 16:
			flag_16 = s[index:index+2]
			print flag_16,
			index += 2
			repeat_value = CL2[-1]
			repeat_times = ( 3 + valueOf(flag_16[::-1]))
			CL2 += [repeat_value] *  repeat_times
			cl2_count += repeat_times
		elif cl2_value == 17:
			flag_17 = s[index:index+3]
			print flag_17,
			index += 3
			repeat_value = 0
			repeat_times = ( 3 + valueOf(flag_17[::-1]))
			CL2 += [repeat_value] * repeat_times
			cl2_count += repeat_times
		elif cl2_value == 18:
			flag_18 = s[index:index+7]
			print flag_18,
			index += 7
			repeat_value = 0
			repeat_times = ( 11 + valueOf(flag_18[::-1]))
			CL2 += [repeat_value] * repeat_times
			cl2_count += repeat_times
		else:
			CL2.append(cl2_value)
			cl2_count += 1
		buff = ""
print "CL2"
print CL2
huffman_tree_outputfile.write("CL2\n")
huffman_tree_outputfile.write(str(CL2))
huffman_tree_outputfile.write("\n")
print "CL2 huffman hash map:(distance)"
huffman_map2 = getMapOfCL2(CL2)
#print huffman_map2
# for code in huffman_map2.keys():
# 	print "%s -> %d"%(code,huffman_map2[code])
huffman_map2_output = open('huffman_map2.txt', 'w')
for code in huffman_map2.keys():
	huffman_map2_output.write(" %s -> %d \n"%(code,huffman_map2[code]))
huffman_map2_output.flush()
huffman_map2_output.close()

#数据段解码
#用于输出
outputBuff = []
dictionary = []
dictionarySize = 32768
outputBuffSize = 1
output = open(CONFIG_OUTPUT_FILENAME, 'wb')
def outputByte(value_int):
	#碰到结尾则立即输出
	if value_int == 256:
		output.write(getBytesFromIntList(outputBuff))
		return
	#value_int在0到255之间，代表一个字节
	if value_int > 127:
		#如果大于127需要转为-128到-1
		value_int = value_int - 256
	#加入到输出缓冲区
	outputBuff.append(value_int)
	#加入到字典
	dictionary.append(value_int)
	#挨个输出已经解码的数据
	# sys.stdout.write(struct.pack('b',value_int))
	if len(dictionary) > dictionarySize:
		#保持字典大小,移除已经不需要在字典里的项
		dictionary.pop(0)
	if len(outputBuff) >= outputBuffSize:
		#说明缓冲区满或者已经到结尾，则进行输出
		output.write(getBytesFromIntList(outputBuff))
		outputBuff[:]=[]
def outputByteWithDistanceAndLength(v_distance,v_length):
	if v_distance > len(dictionary):
		raise Exception("Distance range out of the size of dictionary.")
	segment_start_index = len(dictionary) - v_distance
	for segment_offset in range(v_length):
		value = dictionary[segment_start_index + segment_offset]
		outputByte(value)

data_offset = index
buff = ""
data = []
index = data_offset
while index <= len(s) - 1:
	buff += s[index]
	index += 1
	#看是否已可以读取length或literal
	if huffman_map1.has_key(buff):
		value = huffman_map1[buff]
		if value == 256 :
			#解码已经结束了
			print 'end'
			outputByte(value)
			break
		elif value <= 255:
			#说明是literal，则直接进行输出
			#print "leteral(%s to %d)"%(buff,value) + chr(value)
			value_print = value
			if value_print > 127:
				value_print = value_print - 127
			print "%s(%s)"%(buff,struct.pack('b',value_print)),
			outputByte(value)
		elif value >= 257 and value <= 512:
			#说说明是length，而且后面跟着一个distance，一并取出
			v_length = value - 254
			#print "length(%s to %d)"%(buff,v_length)
			print "%s(%d-length:%d)"%(buff,value,v_length),
			#用来取出distance用的缓冲区
			dst_buff = ""
			while not huffman_map2.has_key(dst_buff):
				#一直取数，直到取出了可以被认为是distance的值为止
				dst_buff += s[index]
				index += 1
			v_distance = huffman_map2[dst_buff]
			print "%s(distance:%d)"%(dst_buff,v_distance),
			#print "distance(%s to %d)"%(dst_buff,v_distance)
			outputByteWithDistanceAndLength(v_distance=v_distance,v_length=v_length)
		else:
			print value
			raise Exception("A value bigger than 256 , but not a distance")
		buff = ""
print index
print len(s)
print buff
output.flush()
output.close()
