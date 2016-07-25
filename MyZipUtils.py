#coding=utf8
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
	if len(cl1) != 285 :
		print 'inflating %d zeros:%d to 285'%(285-len(cl1),len(cl1))
	cl1 += [0] * (285-len(cl1))
	print cl1
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
				print "length: %d"%n
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

def getInfatingBinaray(value,num_of_bits):
	inflating_zeros = num_of_bits - len(bin(value)[2:])
	return '0' * inflating_zeros + bin(value)[2:]