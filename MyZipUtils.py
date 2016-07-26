#coding=utf8
#distance 分区
DISTANCE_GROUP_CODE = [
		[1],
		[2],
		[3],
		[4],
		range(5,7),
		range(7,9),
		range(9,12),
		range(12,17),
		range(17,25),
		range(25,33),
		range(33,49),
		range(49,65),
		range(65,97),
		range(97,129),
		range(129,193),
		range(193,257),
		range(257,385),
		range(385,513),
		range(513,769),
		range(769,1025),
		range(1025,1537),
		range(1537,2049),
		range(2049,3073),
		range(3073,4097),
		range(4097,6145),
		range(6145,8193),
		range(8193,12289),
		range(12289,16385),
		range(16385,24577),
		range(24577,32769)
	]

LENGTH_GROUP_CODE = [
]
def valueOf(bitStrArg):
	return int(bitStrArg,2)
def printCCL(ccl,num_of_ccl):
	clls = []
	print "CLLS: "
	for i in range(0,num_of_ccl):
		item = ccl[i*3:i*3+3][::-1]
		print "%s(%d)"%(item,valueOf(item)),
		clls.append(valueOf(item))
	for i in range(0,19-num_of_ccl):
		print "000(0)",
		clls.append(0)
	print ''
	return clls
def replaceCCL(ccl):
	curren_ccl = []
	curren_ccl.append(ccl[3])
	curren_ccl.append(ccl[17])
	curren_ccl.append(ccl[15])
	curren_ccl.append(ccl[13])
	curren_ccl.append(ccl[11])
	curren_ccl.append(ccl[9])
	curren_ccl.append(ccl[7])
	curren_ccl.append(ccl[5])
	curren_ccl.append(ccl[4])
	curren_ccl.append(ccl[6])
	curren_ccl.append(ccl[8])
	curren_ccl.append(ccl[10])
	curren_ccl.append(ccl[12])
	curren_ccl.append(ccl[14])
	curren_ccl.append(ccl[16])
	curren_ccl.append(ccl[18])
	curren_ccl.append(ccl[0])
	curren_ccl.append(ccl[1])
	curren_ccl.append(ccl[2])
	return curren_ccl
def getMapOfCCL(ccl):
	#cll = [3, 5, 5, 5, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 3]
	#先统计各个code length的个数
	bl_count = {}
	MAX_BITS = max(ccl)
	#为所有2到最大的code length的count都置0
	for bl in range(0,MAX_BITS+1):
		bl_count[bl] = 0
	#统计个数
	for bl in ccl:
		bl_count[bl] += 1
	code = 0;
	bl_count[0] = 0;
	next_code = [0] * (MAX_BITS + 1)
	for bits in range(1,MAX_BITS+1):
		code = (code + bl_count[bits-1])<<1
		next_code[bits] = code
	map_ccl = {}
	#max_code就是ccl的长度
	for n in range(0,len(ccl)):
		n_clen = ccl[n]
		if n_clen != 0:
			#n_clen即为长度
			huffman_code = getInfatingBinaray(next_code[n_clen],n_clen) 
			map_ccl[huffman_code] = n 
			next_code[n_clen] += 1
	return map_ccl
def getMapOfCL1(cl1):
	bl_count = {}
	MAX_BITS = max(cl1)
	#为所有2到最大的code length的count都置0
	for bl in range(0,MAX_BITS+1):
		bl_count[bl] = 0
	#统计个数
	for bl in cl1:
		bl_count[bl] += 1
	code = 0;
	bl_count[0] = 0;
	next_code = [0] * (MAX_BITS + 1)
	for bits in range(1,MAX_BITS+1):
		code = (code + bl_count[bits-1])<<1
		next_code[bits] = code
	map_cl1 = {}
	#max_code就是cl1的长度
	for n in range(0,len(cl1)):
		if n <= 256:
			#说明此处是literal部分,256是结尾符，也当作literal处理
			n_clen = cl1[n]
			if n_clen != 0:
				huffman_code = getInfatingBinaray(next_code[n_clen],n_clen) 
				map_cl1[huffman_code] = n 
				next_code[n_clen] += 1
		else:
			#此处是length部分
			n_clen = cl1[n]
			if n_clen != 0:
				#257代表3，所以减去的值应该是254
				huffman_code = getInfatingBinaray(next_code[n_clen],n_clen) + getExtraBitsOfLength(n-254)
				map_cl1[huffman_code] = n
				next_code[n_clen] += 1
	return map_cl1

def getExtraBitsOfLength(cl1_length):
	if cl1_length in range(3,11):
		return ""
	elif cl1_length in range(11,19):
		return "%d"%(1-cl1_length%2)
	elif cl1_length in range(19,35):
		return getInfatingBinaray((cl1_length - 19)%4,2)
	elif cl1_length in range(35,67):
		return getInfatingBinaray((cl1_length - 35)%8,3)
	elif cl1_length in range(47,131):
		return getInfatingBinaray((cl1_length - 47)%16,4)
	elif cl1_length in range(131,258):
		return getInfatingBinaray((cl1_length - 131)%32,5)
	elif cl1_length == 258:
		return ""

def getMapOfCL2(cl2):
	bl_count = {}
	MAX_BITS = max(cl2)
	#为所有2到最大的code length的count都置0
	for bl in range(0,MAX_BITS+1):
		bl_count[bl] = 0
	#统计个数
	for bl in cl2:
		bl_count[bl] += 1
	code = 0;
	bl_count[0] = 0;
	next_code = [0] * (MAX_BITS + 1)
	for bits in range(1,MAX_BITS+1):
		code = (code + bl_count[bits-1])<<1
		next_code[bits] = code
	map_cl2 = {}
	#max_code就是cl2的长度
	# n 为 distance 所在的区间号的code
	for n in range(0,len(cl2)):
		n_clen = cl2[n]
		if n_clen != 0:
			distance_group = getDistanceGroupByCode(n)
			for distance in distance_group:
				huffman_code = getInfatingBinaray(next_code[n_clen],n_clen) + " " +  getExtraBitsOfDistance(distance)
				map_cl2[huffman_code] = distance
			next_code[n_clen] += 1
	return map_cl2

def getInfatingBinaray(value,num_of_bits):
	inflating_zeros = num_of_bits - len(bin(value)[2:])
	return '0' * inflating_zeros + bin(value)[2:]

def getLengthGroupByCode(code):
	return LENGTH_GROUP_CODE[code]

def getDistanceGroupByCode(code):
	return DISTANCE_GROUP_CODE[code]

def getExtraBitsOfDistance(cl2_distance):
	if cl2_distance in range(1,5):
		return ""
	elif cl2_distance in range(5,9):
		return "%d"%((cl2_distance-5)%2)
	elif cl2_distance in range(9,17):
		return getInfatingBinaray((cl2_distance -9)%4,2)
	elif cl2_distance in range(17,33):
		return getInfatingBinaray((cl2_distance - 17)%8,3)
	elif cl2_distance in range(33,65):
		return getInfatingBinaray((cl2_distance - 33)%16,4)
	elif cl2_distance in range(65,129):
		return getInfatingBinaray((cl2_distance - 65)%32,5)
	elif cl2_distance in range(129,257):
		return getInfatingBinaray((cl2_distance - 129)%64,6)
	elif cl2_distance in range(257,513):
		return getInfatingBinaray((cl2_distance - 257)%128,7)
	elif cl2_distance in range(513,1025):
		return getInfatingBinaray((cl2_distance - 513)%256,8)
	elif cl2_distance in range(1025,2049):
		return getInfatingBinaray((cl2_distance - 1025)%512,9)
	elif cl2_distance in range(2049,4097):
		return getInfatingBinaray((cl2_distance - 2049)%1024,10)
	elif cl2_distance in range(4097,8193):
		return getInfatingBinaray((cl2_distance - 4097)%2048,11)
	elif cl2_distance in range(8193,16385):
		return getInfatingBinaray((cl2_distance - 8193)%4096,12)
	elif cl2_distance in range(16385,32768):
		return getInfatingBinaray((cl2_distance - 4097)%8192,13)
	else:
		raise Exception("Invalid Distance")

