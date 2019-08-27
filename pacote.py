import hashlib


def encrypt_string(data):
	hash_string = str(data)
	sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
	sha = sha_signature[:4]
	int_sha = int(sha, 16)
	sha_final = int_sha.to_bytes(2, "big")
	return sha_final


class info_pacote(object):

	def _init_(self, size, file_size, code, right, data, overhead):

		self.pack_size = size
		self.file_size = file_size
		self.encrypt_code = code
		self.right = right
		self.data = data
		self.overhead = overhead


class pacote(object):

	def _init_(self):
		self.head_size = 14
		self.max_size = 128
		ep = 4059231220
		bs = 67836508785279220
		self.eop = ep.to_bytes(4, "big")
		self.bytes_stuffing = bs.to_bytes(8, "big")

		# head variables
		self.max_pack_size = 4
		self.max_code_size = 2

	def find_eop(self, data):
		for i in range(len(data)):
			if data[i:i+4] == self.eop:
				return i

	def find_false_eop(self, data):
		for i in range(len(data)):
			if data[i:i+8] == self.bytes_stuffing:
				return i

	def fix_bytes_stuffing(self, data):
		while True:
			i = data.find(self.eop)
			if i != None:
				data = data[:i]+self.bytes_stuffing+data[i+4:]
			else:
				break
		return data

	def restore_bytes_stuffing(self, data):
		while True:
			i = self.find_false_eop(data)
			if i != None:
				data = data[:i]+self.eop+data[i+8:]
			else:
				break
		return data

	def head(self, data):
		# tem o tamanho do arquivo mais o eop
		pack_size = len(data)+4
		encrypt_code = encrypt_string(data)
		size_bytes = pack_size.to_bytes(self.max_pack_size, "big")
		complement = bytes(self.head_size-self.max_pack_size-self.max_code_size)
		final_head = size_bytes+complement+encrypt_code

		return final_head

	def read_head(self, data):

		size_bytes = int.from_bytes(
			data[:self.max_pack_size], "big")+self.head_size-self.max_pack_size
		encrypt = data[self.head_size-self.max_code_size:]

		return size_bytes, encrypt

	def empacotar(self, data):
		data = self.fix_bytes_stuffing(data)
		self.pack = self.head(data)+data+self.eop
		return self.pack

	def ler_pacotes(self, pacote):

		size_bytes, encrypt = self.read_head(pacote[:self.head_size])

		eop_i = self.find_eop(pacote)

		data = self.restore_bytes_stuffing(pacote[self.head_size:eop_i])

		if self.find_eop(pacote) == size_bytes+self.max_pack_size-4:
			print("EOP no lugar certo")
		elif self.find_eop(pacote):
			print(not self.find_eop(pacote), self.find_eop(pacote))
			print("EOP no lugar errado, o índice é: {}".format(self.find_eop(pacote)))
		else:
			print("EOP não encontrado")

		size_file = len(data)

		right = (encrypt == encrypt_string(data))

		overhead = (size_bytes-4-self.head_size+self.max_pack_size) / \
                    (size_bytes+self.max_pack_size)

		info_packs = info_pacote(size_bytes, size_file,
		                         encrypt, right, data, overhead)

		return info_packs
