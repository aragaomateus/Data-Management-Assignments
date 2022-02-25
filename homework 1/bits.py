# Part 1 goes here!
class DecodeError(Exception):
    pass
class ChunkError(Exception):
    pass
class BitList:
    def __init__(self,bits):
        #set(bits) not in('0','1')
        if not set(bits).issubset({'0','1'}):
            raise ValueError("Invalid Characters")
        self.bits = bits
        self.bit_list = [int(bit) for bit in list(bits.strip(''))]
        
    @staticmethod 
    def from_ints(*args):
        bits = ''
        try:
            bits = ''.join(map(str,args))
        except ValueError:
            print("not 0 or 1")
        return BitList(bits)
    def __eq__(self, other):
        if self.bit_list == other.bit_list:
            return True
        else:
            return False
    def __str__(self):
        return self.bits
    def arithmetic_shift_left(self):
        self.bit_list.remove(self.bit_list[0])
        self.bit_list.append(0)
        temp = [str(bit) for bit in self.bit_list]
        self.bits = ''.join(temp)
    def arithmetic_shift_right(self):
        self.bit_list.pop()
        self.bit_list.insert(0,self.bit_list[0])
        temp = [str(bit) for bit in self.bit_list]
        self.bits = ''.join(temp)    
    def bitwise_and(self,other):
        # returns a bitlist instance
        if len(self.bit_list) != len(other.bit_list):
            raise ValueError("Different length")
        new_bits=''
        for num1, num2 in zip(self.bit_list,other.bit_list):
            new_bits+=str(num1*num2)
        return BitList(new_bits)
    def chunk(self,chunk_length):
        if len(self.bit_list)%chunk_length != 0:
            raise ChunkError ("Chunk legth wont match")
        chunks = []
        chunk = []
        print(len(self.bit_list))
        for bit in self.bit_list:
            chunk.append(bit)
            if len(chunk) == chunk_length:
                chunks.append(chunk)
                chunk = []
                
        return chunks
    def decode(self,encoding = 'utf-8'):
        if encoding not in ('utf-8','us-ascii'):
            raise ValueError("Invalid encoding type")
    
    def decode(self, encoding='utf-8'):
        if encoding not in {'utf-8', 'us-ascii'}:
            raise ValueError("Invalid encoding")
        if (encoding == 'us-ascii'):
            byte_list = list(map(''.join, zip(*[iter(self.bits)]*7)))
            encoded_list = [chr(int(x, 2)) for x in byte_list]
            return ''.join(str(e) for e in encoded_list)
        elif (encoding == 'utf-8'):
            try:
                bytes_as_bin = list(self.bits[i: i + 8] for i in range(0, len(self.bits), 8))
                b = bytes([int(i, 2) for i in bytes_as_bin])
                return b.decode('utf-8')  
            except DecodeError:
                print("invalid continuation byte or invalid start byte")        
   
        
    
bits = BitList.from_ints(1, 1, 0, 0, 0, 0, 1)
ch = bits.decode('us-ascii')
print(ch)

b = BitList('11110000100111111001100010000010111000101000001010101100')
s = b.decode('utf-8')
print(s)


