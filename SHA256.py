import bitarray
import numpy as np
from operator import add

# Convert to bits

def bin_32bit(dec):
	return(str(format(dec,'032b')))

def tobits(string):

	result = list(''.join(format(ord(x), 'b') for x in string))
	result_list = list(result)
	results = map(int, result_list)

	return results

def padding(string):
	bits = tobits(string)
	L = len(bits)
	bits.append(1)
	
	L_bit = [int(i) for i in format(L,'064b')]

	K = 0
	while ((L+1+K)-448)%512 != 0:
		K+=1

	K_zeros = [0]*K
	bits.extend(K_zeros)
	bits.extend(L_bit)

	return bits

def big_chunks(l, n = 512):

	big_chunks = []
	for i in range(0, len(l), n):  
		big_chunks.append(l[i:i + n])

	return big_chunks

def chunks(l, n = 16):

	array = np.array_split(l,n)

	list_chunks = []
	for i in array:
		list_chunks.append(i.tolist())

	return list_chunks

# Set up functions
	
def right_rotate(l,n):

	rot_value = l[-n:]
	remain = l[:-n]
	new_list = rot_value + remain

	return new_list

def right_shift(l,n):
	
	remain = l[:-n]
	new_list = [0]*n + remain

	return new_list

def bit_comp(x):
	for i in range(0,len(x)):
		if x[i] == 1:
			x[i] = 0
		if x[i] == 0:
			x[i] = 1
	return x

def ch(X,Y,Z):
	X = bit_comp(X)
	return (xor(and_bool(X,Y),and_bool(X,Z)))

def Maj(X,Y,Z):

	result = xor(and_bool(X,Y),and_bool(X,Z))

	return xor(result,and_bool(Y,Z))

def sig0(bit_list):

	list_1 = right_rotate(bit_list,7)
	list_2 = right_rotate(bit_list,18)
	list_3 = right_shift(bit_list,3)

	result_list = xor(list_1,list_2)
	result_list = xor(result_list,list_3)

	return result_list

def sig1(bit_list):

	list_1 = right_rotate(bit_list,17)
	list_2 = right_rotate(bit_list,19)
	list_3 = right_shift(bit_list,10)

	result_list = xor(list_1,list_2)
	result_list = xor(result_list,list_3)

	return result_list

def sum0(bit_list):

	list_1 = right_rotate(bit_list,2)
	list_2 = right_rotate(bit_list,13)
	list_3 = right_rotate(bit_list,22)

	result_list = xor(list_1,list_2)
	result_list = xor(result_list,list_3)

	return result_list

def sum1(bit_list):

	list_1 = right_rotate(bit_list,6)
	list_2 = right_rotate(bit_list,11)
	list_3 = right_rotate(bit_list,25)

	result_list = xor(list_1,list_2)
	result_list = xor(result_list,list_3)

	return result_list


def xor(l_1,l_2):

	xor_list=[]

	for i in range(len(l_1)):

		if l_1[i]==0 and l_2[i]==0:
			xor_list.append(0)
		if l_1[i]==1 and l_2[i]==1:
			xor_list.append(0)
		if l_1[i]==0 and l_2[i]==1:
			xor_list.append(1)
		if l_1[i]==1 and l_2[i]==0:
			xor_list.append(1)

	return xor_list


def and_bool(l_1,l_2):

	and_list=[]

	for i in range(len(l_1)):

		if l_1[i]==1 and l_2[i]==1:
			and_list.append(1)
		else:
			and_list.append(0)

	return and_list


def or_bool(l_1,l_2):

	or_list=[]

	for i in range(len(l_1)):
		if l_1[i]==0 and l_2[i]==0:
			or_list.append(0)
		else:
			or_list.append(1)

	return or_list

def mod_32_addition(input_set):
	value=0

	for i in range(len(input_set)):
		l_int = int((''.join(str(i) for i in input_set[i])),2)
		value+=l_int

	mod_32 = 4294967296
	result_str = bin_32bit(value%mod_32)

	result = [int(i) for i in result_str]

	return result

"""

Block Decomposition

"""

def decomp(bits):

	for i in range(17,65):

		W1 = sig1(bits[i-2])
		W2 = bits[i-7]
		W3 = sig0(bits[i-15])
		W4 = bits[i-16]

		bits.append(mod_32_addition([W1, W2, W3, W4]))

	return bits

def hex2dec(hex_c):

	dec = bin_32bit(int(hex_c, 16))
	result = [int(i) for i in str(dec)]

	return result

"""

Hash Computation

"""

class sha():
	"""docstring for sha"""
	def __init__(self):
		pass


	def sha256(self, Input_String):


		# Initialize hash values

		a = '6a09e667'
		b = 'bb67ae85'
		c = '3c6ef372'
		d = 'a54ff53a'
		e = '510e527f'
		f = '9b05688c'
		g = '1f83d9ab'
		h = '5be0cd19'

		hex_cons = [a, b, c, d, e, f, g, h]

		# Initialize array of constants
		cons=[
				'428a2f98','71374491','b5c0fbcf','e9b5dba5',
				'3956c25b','59f111f1','923f82a4','ab1c5ed5',
				'd807aa98','12835b01','243185be','550c7dc3',
				'72be5d74','80deb1fe','9bdc06a7','c19bf174',
				'e49b69c1','efbe4786','0fc19dc6','240ca1cc',
				'2de92c6f','4a7484aa','5cb0a9dc','76f988da',
				'983e5152','a831c66d','b00327c8','bf597fc7',
				'c6e00bf3','d5a79147','06ca6351','14292967',
				'27b70a85','2e1b2138','4d2c6dfc','53380d13',
				'650a7354','766a0abb','81c2c92e','92722c85',
				'a2bfe8a1','a81a664b','c24b8b70','c76c51a3',
				'd192e819','d6990624','f40e3585','106aa070',
				'19a4c116','1e376c08','2748774c','34b0bcb5',
				'391c0cb3','4ed8aa4a','5b9cca4f','682e6ff3',
				'748f82ee','78a5636f','84c87814','8cc70208',
				'90befffa','a4506ceb','bef9a3f7','c67178f2'
			  ]

		for i in range(0,len(hex_cons)):
			hex_cons[i] = hex2dec(hex_cons[i])

		for i in range(0,len(cons)):
			cons[i] = hex2dec(cons[i])

		big = big_chunks(padding(Input_String))

		for i in big:
			new_bits = decomp(chunks(i))

			ihex = hex_cons[:]

			for j in range(0,64):
				T1 = mod_32_addition([ihex[7],sum1(ihex[4]),ch(ihex[4],ihex[5],ihex[6]),\
								 	 cons[j],new_bits[j]])
				T2 = mod_32_addition([sum0(ihex[0]),Maj(ihex[0],ihex[1],ihex[2])])
				ihex[7] = ihex[6]
				ihex[6] = ihex[5]
				ihex[5] = ihex[4]
				ihex[4] = mod_32_addition([ihex[3],T1])
				ihex[3] = ihex[2]
				ihex[2] = ihex[1]
				ihex[1] = ihex[0]
				ihex[0] = mod_32_addition([T1,T2])

			for k in range(0,len(hex_cons)):
				hex_cons[k] = mod_32_addition([hex_cons[k],ihex[k]])


		sha_output_list = []
		for i in range(0,len(hex_cons)):
			hex_int = int(''.join([str(bit) for bit in hex_cons[i]]),2)
			hex_bin = format(hex_int,'x')
			sha_output_list.append(hex_bin)


		sha_output_string = ''.join([(i) for i in sha_output_list])
		
		return sha_output_string




















