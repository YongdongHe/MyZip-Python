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
			huffman_code = next_code[n_clen]
			if huffman_code == 0:
				map_ccl["00"] = n 
			elif huffman_code == 1:
				map_ccl["01"] = n 
			else:
				map_ccl[bin(huffman_code)[2:]] = n 
			next_code[n_clen] += 1
	return map_ccl

MARK16 = 16
MARK17 = 17
MARK18 = 18

