"""
-----------------------------
PSUT: Cryptography (Fall 2022)
Name: Yazan Masalha
ID:   20200736
Assignment4
# notes: some problems in set_key
-----------------------------
"""
import math

import utilities


class PRNG:
    """
    ----------------------------------------------------
    Description: Pseudo random number generators
    ----------------------------------------------------
    """
    PRIMES_FILE = 'primes.txt'

    @staticmethod
    def BBS(p,q,bits):
        """
        ----------------------------------------------------
        Parameters:   p (int): a prime number
                      q (int): a prime number
                      bits (int): number of bits to generate
        Return:       output (str): random binary bits
        Description:  Blum Blum Shub PRNG Generator
                      p and q should be primes congruent to 3
                      The seed is the nth prime number, where n = p*q
                      If the nth prime number is not relatively prime with n,
                          the next prime number is selected until a valid one is found
                          The prime numbers are read from the file PRIMES_FILE (starting n=1)
                      If invalid input --> return error message
        ---------------------------------------------------
        """ 
        # your code here
        if p <= 0 or p % 4 != 3 or type(p) != int:
            return "Error(PRNG.BBS): invalid p"
        if q <= 0 or q % 4 != 3 or type(q) != int:
            return "Error(PRNG.BBS): invalid q"
        if bits <= 0 or type(bits) != int:
            return "Error(PRNG.BBS): invalid bits"

        the_bits = ""
        n = p * q
        with open("primes.txt") as f:
            primes = f.read().strip("\n").split()
        s = n
        i = primes[n - 1]
        while not MOD.is_relatively_prime(n, i):
            i = primes[s]
            s += 1

        x = int(i) ** 2 % n
        for i in range(1, bits + 1):
            x = x ** 2 % n
            b = x % 2
            the_bits += str(b)
        return the_bits

class SBOX:
    """
    ----------------------------------------------------
    Description: SDES SBOX
    ----------------------------------------------------
    """
    def __init__(self, filename=""):
        """
        ----------------------------------------------------
        Parameters:   _box (list): default value = [[],[]]
                      _size (int): #bits for input, default = 0
        Description:  Creates an SBOX from a given file
                      The contents of the file are read into a 2D list
                      The size represent #bits for the sbox input
                      Note that the output #bits is (size - 1)
        ---------------------------------------------------
        """
        # your code here
        self._size = 0
        self.set_box(filename)

    
    def is_empty(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  Check if current sbox is empty
        ---------------------------------------------------
        """ 
        # your code here
        if self._box[0] or self._box[1]:
            return False
        return True
    
    def get_box(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       box (list)
        Description:  Returns a copy of _box
                      Use deepcopy from copy library
        ---------------------------------------------------
        """ 
        # your code here
        return self._box
    
    def get_size(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       size (int)
        Description:  Returns a copy of current sbox size
        ---------------------------------------------------
        """ 
        # your code here
        return self._size
    
    def set_box(self,filename):
        """
        ----------------------------------------------------
        Parameters:   filename (str)
        Return:       no return
        Description:  Read contents of a file into _box
                      file is formatted as:
                        <item[0][0]>-<item[0][1]>-...-<item[0][n-1]>
                        <item[1][0]>-<item[1][1]>-...-<item[1][n-1]>
                      where n is the size
                      update values of _box and _size
                      assume that the file always has valid content
        ---------------------------------------------------
        """ 
        # your code here
        if filename == "":
            self._box = [[], []]
        else:
            with open(filename) as f:
                content = f.read()
            sc = content.strip("\n").split()
            bc = [sc[0].split("-"), sc[1].split("-")]
            self._box = bc
            self._size = len(str(self._box[0][0])) + 1
        return None
    
    def substitute(self,value):
        """
        ----------------------------------------------------
        Parameters:   value (str): sbox input (binary num of size bits)
        Return:       result (str): sbox output (binary num of size-1 bits)
        Description:  substitute <value> to corresponding output in sbox
                      if invalid input return ''
        ---------------------------------------------------
        """ 
        # your code here
        if self.is_empty() or type(value) != str or len(value) != 4:
            return ""
        return str(self._box[int(value[0])][utilities.bin_to_dec(value[1::])])
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of SBOX object
                      format:
                      SBOX(<size>):
                      <_box[0]>
                      <_box[1]>
        ---------------------------------------------------
        """ 
        # your code here
        whole_string = f"SBOX({self._size}):\n{self._box[0]}\n{self._box[1]}"
        return whole_string

class SDES:
    DEFAULT_ENCODING = 'B6'
    DEFAULT_BLOCK_SIZE = 12
    DEFAULT_KEY_LENGTH = 9
    DEFAULT_ROUNDS = 2
    DEFAULT_P = 103
    DEFAULT_Q = 199
    DEFAULT_SBOX1 = SBOX('sbox1.txt')
    DEFAULT_SBOX2 = SBOX('sbox2.txt')
    DEFAULT_PAD = 'Q'

    def __init__(self):
        """
        ----------------------------------------------------
        Parameters:   _rounds (int)
                      _key_length (int)
                      _block_size (int)
                      _encoding (str): set to B6
                      _p (int)
                      _q (int)
                      _sbox1 (SBOX)
                      _sbox2 (SBOX)
                      _pad (str)
        Description:  Constructs an SDES object
                      All parameters are set to default values
        ---------------------------------------------------
        """
        # your code here
        self._rounds = self.DEFAULT_ROUNDS
        self._key_length = self.DEFAULT_KEY_LENGTH
        self._block_size = self.DEFAULT_BLOCK_SIZE
        self._encoding = self.DEFAULT_ENCODING
        self._p = self.DEFAULT_P
        self._q = self.DEFAULT_Q
        self._sbox1 = self.DEFAULT_SBOX1
        self._sbox2 = self.DEFAULT_SBOX2
        self._pad = self.DEFAULT_PAD

        
    def get_value(self,parameter):
        """
        ----------------------------------------------------
        Parameters:   parameter (str)
        Return:       value (?)
        Description:  Returns a copy of parameter value
                      Valid parameter names:
                      rounds, key_length, block_size
                      encoding, p, q, sbox1, sbox2, pad
                      if invalid parameter name --> print error msg & return ''
        ---------------------------------------------------
        """
        # your code here
        if parameter == "rounds":
            return self._rounds
        if parameter == "key_length":
            return self._key_length
        if parameter == "block_size":
            return self._block_size
        if parameter == "encoding":
            return self._encoding
        if parameter == "p":
            return self._p
        if parameter == "q":
            return self._q
        if parameter == "sbox1":
            return self._sbox1
        if parameter == "sbox2":
            return self._sbox2
        if parameter == "pad":
            return self._pad
        print("Error(SDES.get_value): undefined parameter")
        return ""

    def set_parameter(self,parameter,value):
        """
        ----------------------------------------------------
        Parameters:   parameter (str)
                      value (?)
        Return:       success: True/False
        Description:  Set the given parameter to given value (if valid)
                      if invalid value, do not update current value
                      if invalid parameter name, print error msg and return ''
                      rounds should be an integer larger than 1
                      p and q should be integers congruent to 3 mod 4
                      pad should be a single character string in B6 encoding
                      sbox1 and sbox2 should be non-empty SBOX objects
                      block_size should be an integer of multiples of 2, >= 4
                          sets also key_length to block_size//2 + 3
                      cannot set key_length directly
                      If invalid value, return False
                      if invalid parameter name, print error msg and return False
        ---------------------------------------------------
        """
        # your code here
        if parameter == "rounds":
            if value > 1 and type(value) == int:
                self._rounds = value
                return True
            else:
                return False
        if parameter == "key_length":
            if value != (self._block_size / 2) + 3:
                print("Error(SDES.set_parameter): undefined operation")
                return False
            self._key_length = value
            return True
        if parameter == "block_size":
            if value != 12 or type(value) != int:
                return False
            self._block_size = value
            self._key_length = (self._block_size / 2) + 3
            return True
        if parameter == "encoding":
            if value != "B6":
                return False
            self._encoding = value
            return True
        if parameter == "p":
            if type(value) != int or value % 4 != 3 or not MOD.is_prime(value):
                return False
            self._p = value
            return True
        if parameter == "q":
            if type(value) != int or value % 4 != 3 or not MOD.is_prime(value):
                return False
            self._q = value
            return True
        if parameter == "sbox1":
            if value.is_empty():
                return False
            self._sbox1 = value
            return True
        if parameter == "sbox2":
            if value.is_empty():
                return False
            self._sbox2 = value
            return True
        if parameter == "pad":
            if type(value) != str or len(value) != 1 or value not in utilities.get_base("B6"):
                return False
            self._pad = value
            return True
        print("Error(SDES.set_parameter): undefined operation")
        return False

    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (str): binary number
        Description:  Returns a copy of SDES key
                      The key is generated by Blum Blum Shub algorithm
                      Uses p and q to generates key_length bits
        ---------------------------------------------------
        """
        # your code here
        return PRNG.BBS(self._p, self._q, self._key_length)
    
    def get_subkey(self,i):
        """
        ----------------------------------------------------
        Parameters:   i (int): subkey index
        Return:       subkey (str): binary number
        Description:  Returns the ith subkey from SDES key
                      Gets key_length bits from key starting at index i
                      Using circular indexing if necessary
        Errors:       if invalid i --> return ''
        ---------------------------------------------------
        """
        # your code here
        if i <= 0:
            return ""
        key = self.get_key()
        the_key = [key[(i + j - 1) % self._key_length] for j in range(self._key_length - 1)]
        return "".join(the_key)
        
    def expand(self,R):
        """
        ----------------------------------------------------
        Parameters:   R (str): binary number of size (block_size/2)
        Return:       R_exp (str): output of expand function
        Description:  Expand the input binary number by adding two digits
                      Expansion works as the following:
                      If the index of the two middle elements is i and i+1
                          indices 0 up to i-1: same order
                          middle becomes: R(i+1)R(i)R(i+1)R(i)
                          indices R(i+2) to the end: same order
                      No need to validate that R is of size block_size/2
        Errors:       if R is an invalid binary number -->  return ''
        ---------------------------------------------------
        """
        # your code here
        if not utilities.is_binary(R):
            return ''
        mid_idx = (len(R) // 2) - 1
        R_exp = ""
        for i in range(mid_idx):
            R_exp += R[i]
        R_exp += R[mid_idx + 1]
        R_exp += R[mid_idx]
        R_exp += R[mid_idx + 1]
        R_exp += R[mid_idx]
        for i in range(mid_idx + 2, len(R)):
            R_exp += R[i]
        return R_exp
    
    def F(self,Ri,ki):
        """
        ----------------------------------------------------
        Parameters:   Ri (str): block of binary numbers
                      ki (str): binary number representing subkey
        Return:       Ri2 (str): block of binary numbers
        Description:  Performs the following five tasks:
                      1- Pass the Ri block to the expander function
                      2- Xor the output of [1] with ki
                      3- Divide the output of [2] into two equal sub-blocks
                      4- Pass the most significant bits of [3] to Sbox1
                         and least significant bits to sbox2
                      5- Concatenate the output of [4] as [sbox1][sbox2]
        Errors:       if ki or Ri is an invalid binary number --> return ''
        ---------------------------------------------------
        """
        # your code here
        if not utilities.is_binary(Ri) or not utilities.is_binary(ki) or len(ki) != len(Ri) + 2:
            return ""
        R_exp = self.expand(Ri)
        xored = utilities.xor(R_exp, ki)
        xored_blocks = [[xored[i] for i in range(len(xored) // 2)], [xored[i] for i in range(len(xored) // 2, len(xored))]]
        most_sig_bits = "".join(xored_blocks[0])
        least_sig_bits = "".join(xored_blocks[1])
        ans = self._sbox1.substitute(most_sig_bits) + self._sbox2.substitute(least_sig_bits)
        return ans

    def feistel(self,bi,ki):
        """
        ----------------------------------------------------
        Parameters:   bi (str): block of binary numbers
                      ki (str): binary number representing subkey
        Return:       bi2 (str): block of binary numbers
        Description:  Applies Feistel Cipher on a block of binary numbers
                      L(current) = R(previous)
                      R(current) = L(previous) xor F(R(previous), subkey)
        Errors:       if ki or bi is an invalid binary number --> return ''
        ---------------------------------------------------
        """
        # your code here
        if  (len(bi) / 2) + 2 != len(ki) or not utilities.is_binary(bi) or not utilities.is_binary(ki):
            return ''
        blocks = [[bi[i] for i in range(len(bi) // 2)],
                        [bi[i] for i in range(len(bi) // 2, len(bi))]]
        li = "".join(blocks[1])
        ri = utilities.xor("".join(blocks[0]), self.F(li, ki))
        return li + ri
    
    def encrypt(self,plaintext,mode):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
                      mode (str)
        Return:       ciphertext (str)
        Description:  A dispatcher SDES encryption function
                      passes the plaintext to the proper function based on given mode
                      Works for ECB and CBC modes
        Errors:       if undefined mode --> return ''
        ---------------------------------------------------
        """
        # your code here
        if mode == "ECB":
            return self._encrypt_ECB(plaintext)
        elif mode == "CBC":
            return self._encrypt_CBC(plaintext)
        else:
            return ""
    
    def decrypt(self,ciphertext,mode):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
                      mode (str)
        Return:       plaintext (str)
        Description:  A dispatcher SDES decryption function
                      passes the ciphertext to the proper function based on given mode
                      Works for ECB and CBC modes
        Errors:       if undefined mode --> return ''
        ---------------------------------------------------
        """
        # your code here
        if mode == "ECB":
            return self._decrypt_ECB(ciphertext)
        elif mode == "CBC":
            return self._decrypt_CBC(ciphertext)
        else:
            return ""
    
    def _encrypt_ECB(self,plaintext):
        # your code here
        ciphertext = ""
        last_cipher = ""
        base = utilities.get_base("B6")
        not_in_base = [i for i in plaintext if i not in base]
        not_in_base = "".join(not_in_base)
        positions = utilities.get_positions(plaintext, not_in_base)
        cleaned_text = utilities.clean_text(plaintext, not_in_base)
        if len(cleaned_text) % 2 != 0:
            cleaned_text += self._pad
        for i in range(0, len(cleaned_text) - 1, 2):
            first_one = utilities.encode(cleaned_text[i], "B6")
            second_one = utilities.encode(cleaned_text[i + 1], "B6")
            ans = first_one + second_one
            for i in range(self._rounds):
                ans = self.feistel(ans, self.get_subkey(i + 1))
            ans = ans[len(ans) // 2::] + ans[0:len(ans) // 2]
            ciphertext += ans
        for i in range(0, len(ciphertext), 6):
            # print(f"bobo --> {i}, {i + 6}")
            last_cipher += utilities.decode(ciphertext[i: i + 6], "B6")
        final = utilities.insert_positions(last_cipher, positions)
        return final
    
    def _decrypt_ECB(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using ECB mode
        ---------------------------------------------------
        """
        # your code here
        plaintext = ""
        last_plain = ""
        base = utilities.get_base("B6")
        not_in_base = [i for i in ciphertext if i not in base]
        not_in_base = "".join(not_in_base)
        positions = utilities.get_positions(ciphertext, not_in_base)
        cleaned_text = utilities.clean_text(ciphertext, not_in_base)
        if len(cleaned_text) % 2 != 0:
            cleaned_text += self._pad
        for i in range(0, len(cleaned_text) - 1, 2):
            first_one = utilities.encode(cleaned_text[i], "B6")
            second_one = utilities.encode(cleaned_text[i + 1], "B6")
            ans = first_one + second_one
            for i in range(self._rounds, 0, -1):
                ans = self.feistel(ans, self.get_subkey(i))
            ans = ans[len(ans) // 2::] + ans[0:len(ans) // 2]
            plaintext += ans
        for i in range(0, len(plaintext), 6):
            # print(f"bobo --> {i}, {i + 6}")
            last_plain += utilities.decode(plaintext[i: i + 6], "B6")
        final = utilities.insert_positions(last_plain, positions)
        to_ = len(final) - 1
        while final[to_] == self._pad:
            to_ -= 1
        return final[0:to_ + 1]

    def _encrypt_CBC(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using CBC mode
        ---------------------------------------------------
        """ 
        # your code here
        ciphertext = ""
        last_cipher = ""
        base = utilities.get_base("B6")
        not_in_base = [i for i in plaintext if i not in base]
        not_in_base = "".join(not_in_base)
        positions = utilities.get_positions(plaintext, not_in_base)
        cleaned_text = utilities.clean_text(plaintext, not_in_base)
        previous_c = self._get_IV()
        if len(cleaned_text) % 2 != 0:
            cleaned_text += self._pad
        for i in range(0, len(cleaned_text) - 1, 2):
            first_one = utilities.encode(cleaned_text[i], "B6")
            second_one = utilities.encode(cleaned_text[i + 1], "B6")
            ans = first_one + second_one
            xored_input = utilities.xor(ans, previous_c)
            for i in range(self._rounds):
                xored_input = self.feistel(xored_input, self.get_subkey(i + 1))
            xored_input = xored_input[len(xored_input) // 2::] + xored_input[0:len(xored_input) // 2]
            ciphertext += xored_input
            previous_c = xored_input
        for i in range(0, len(ciphertext), 6):
            # print(f"bobo --> {i}, {i + 6}")
            last_cipher += utilities.decode(ciphertext[i: i + 6], "B6")
        final = utilities.insert_positions(last_cipher, positions)
        return final

    def _get_IV(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       iv (str): binary number
        Description:  prepares an IV for CBC and OFB modes
                      the IV length is the same as the block size
                      the IV is a stream of bits that follow the following pattern:
                      1 00 111 0000 11111 ...
        ---------------------------------------------------
        """
        ans = ""
        for i in range(self._block_size):
            if i % 2 == 0:
                ans += "1" * (i + 1)
            else:
                ans += "0" * (i + 1)
        iv = ans[0:self._block_size]
        return iv

    def _decrypt_CBC(self,ciphertext):   
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using CBC mode
        ---------------------------------------------------
        """     
        # your code here
        plaintext = ""
        last_plain = ""
        base = utilities.get_base("B6")
        not_in_base = [i for i in ciphertext if i not in base]
        not_in_base = "".join(not_in_base)
        positions = utilities.get_positions(ciphertext, not_in_base)
        cleaned_text = utilities.clean_text(ciphertext, not_in_base)
        previous_c = self._get_IV()
        if len(cleaned_text) % 2 != 0:
            cleaned_text += self._pad
        for i in range(0, len(cleaned_text) - 1, 2):
            first_one = utilities.encode(cleaned_text[i], "B6")
            second_one = utilities.encode(cleaned_text[i + 1], "B6")
            ans = first_one + second_one
            for i in range(self._rounds, 0, -1):
                ans = self.feistel(ans, self.get_subkey(i))
            ans = ans[len(ans) // 2::] + ans[0:len(ans) // 2]
            xored_input = utilities.xor(ans, previous_c)
            plaintext += xored_input
            previous_c = first_one + second_one
        for i in range(0, len(plaintext), 6):
            # print(f"bobo --> {i}, {i + 6}")
            last_plain += utilities.decode(plaintext[i: i + 6], "B6")
        final = utilities.insert_positions(last_plain, positions)
        to_ = len(final) - 1
        while final[to_] == self._pad:
            to_ -= 1
        return final[0:to_ + 1]

'______________________________________________________________'

# put your mode class here

class MOD:
    """
    ----------------------------------------------------
    Description: Some utility functions for modular arithmetic
    ----------------------------------------------------
    """
    @staticmethod
    def is_prime(n):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   n (int): an arbitrary integer
        Return:       True/False
        Description:  Check if the given input is a prime number
                      Search Online for an efficient implementation
        ---------------------------------------------------
        """
        # your code here
        if n <= 1:
            return False
        if n == 2:
            return True
        for i in range(2, math.ceil(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       result (int): gcd(a,b)
        Description:  Computes and returns the greatest common divider using
                      the standard Eculidean Algorithm.
                      The implementation can be iterative or recursive
        Errors:       if a or b are non positive integers, return:
                        'Error(MOD.gcd): invalid input'
        ---------------------------------------------------
        """
        # your code here
        if type(a) != int or type(b) != int:
            return "Error(MOD.gcd): invalid input"
        if a == 0 or b == 0:
            return "Error(MOD.gcd): invalid input"
        while b != 0:
            t = b
            b = a % b
            a = t
        return abs(a)
        # u = abs(a)
        # v = abs(b)
        # if v > u:
        #     u, v = v, u
        # while v != 0:
        #     q = u // v
        #     r = u - q * v
        #     u = v
        #     v = r
        # return v


    @staticmethod
    def is_relatively_prime(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       True/False
        Description:  Check if <a> and <b> are relatively prime
                          i.e., gcd(a,b) equals 1
        Errors:       if <a> or <b> are non positive integers, return:
                        'Error(Mod.is_relatively_prime): invalid input'
        ---------------------------------------------------
        """
        # your code here
        if type(a) != int or type(b) != int:
            return "Error(MOD.is_relatively_prime): invalid input"
        if a == 0 or b == 0:
            return False
        if MOD.gcd(a, b) == 1:
            return True
        else:
            return False

    @staticmethod
    def has_mul_inv(a, m):
        """
        ----------------------------------------------------
        Parameters:   a (int): an arbitrary positive integer
                      m (int): an arbitrary positive integer
        Return:       True/False
        Description:  Check if <a> has a multiplicative inverse mod <m>
        ---------------------------------------------------
        """
        # your code here
        return MOD.is_relatively_prime(a, m)


    @staticmethod
    def EEA(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       result (list): [gcd(a,b), s, t]
        Description:  Uses Extended Euclidean Algorithm to find:
                        gcd(a,b) and <s> and <t> such that:
                        as + bt = gcd(a,b), i.e., Bezout's identity
        Errors:       if a or b are 0 or non-integers
                        'Error(MOD.EEA): invalid input'
        ---------------------------------------------------
        """
        # your code here
        if a == 0 or b == 0:
            return 'Error(MOD.EEA): invalid input'
        u = [abs(a), 1, 0]
        v = [abs(b), 0, 1]
        while v[0] != 0:
            q = math.floor(u[0] / v[0])
            r = [u[0] - q * v[0], u[1] - q * v[1], u[2] - q * v[2]]
            u = v
            v = r
        return u

    @staticmethod
    def get_mul_inv(a,m):
        """
        ----------------------------------------------------
        Parameters:   a (int): an arbitrary positive integer
                      m (int): an arbitrary positive integer
        Return:       mul_inv (int or 'NA')
        Description:  Computes and returns the multiplicative inverse of
                        current of a mod m
                      if it does not exist returns 'NA'
        Errors:       if a is not a positive integer, or
                      m is not an integer > 1 -->
                      return 'Error(MOD.get_mult_inv): invalid input'
        ---------------------------------------------------
        """
        # your code here
        if m > a:
            t = m
            m = a
            a = t
        if a < 1 or m < 1:
            return 'Error(MOD.get_mult_inv): invalid input'
        res = MOD.EEA(a, m)
        if res[0] != 1:
            return "NA"
        return res[2] % a


sb = SBOX()
sb.set_box('sbox1.txt')
