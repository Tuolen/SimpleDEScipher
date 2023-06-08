from math import ceil

DICT_FILE = 'engmix.txt'
PAD = 'q'

'______________________________________________________________________________'

def get_base(base_type):
    """
    ----------------------------------------------------
    Parameters:   base_type (str) 
    Return:       result (str)
    Description:  Return a base string containing a subset of ASCII charactes
                  Defined base types:
                  lower, upper, alpha, lowernum, uppernum, alphanum, special, nonalpha, B6, BA, all
                      lower: lower case characters
                      upper: upper case characters
                      alpha: upper and lower case characters
                      lowernum: lower case and numerical characters
                      uppernum: upper case and numerical characters
                      alphanum: upper, lower and numerical characters
                      special: punctuations and special characters (no white space)
                      nonalpha: special and numerical characters
                      B6: lower, uppper, num, dot, space
                      BA: upper + lower + num + special + ' \n'
                      all: upper, lower, numerical and special characters
    Errors:       if invalid base type, print error msg, return empty string
    ---------------------------------------------------
    """
    lower = "".join([chr(ord('a')+i) for i in range(26)])
    upper = lower.upper()
    num = "".join([str(i) for i in range(10)])
    special = ''
    for i in range(ord('!'),127):
        if not chr(i).isalnum():
            special+= chr(i)
            
    result = ''
    if base_type == 'lower':
        result = lower
    elif base_type == 'upper':
        result = upper
    elif base_type == 'alpha':
        result = upper + lower
    elif base_type == 'lowernum':
        result = lower + num
    elif base_type == 'uppernum':
        result = upper + num
    elif base_type == 'alphanum':
        result = upper + lower + num
    elif base_type == 'special':
        result = special
    elif base_type == 'nonalpha':
        result = special + num
    elif base_type == 'B6': #64 symbols
        result = lower + upper + num + '.' + ' '
    elif base_type == 'BA': #96 symbols
        result = upper + lower + num + special + ' \n'
    elif base_type == 'all':
        result = upper + lower + num + special
    else:
        print('Error(get_base): undefined base type')
        result = ''
    return result

'______________________________________________________________________________'

def get_language_freq(language='English'):
    """
    ----------------------------------------------------
    Parameters:   language (str): default = English 
    Return:       freq (list of floats) 
    Description:  Return frequencies of characters in a given language
                  Current implementation supports English language
                  If unsupported language --> print error msg and return []
    ---------------------------------------------------
    """
    if language == 'English':
        return [0.08167,0.01492,0.02782, 0.04253, 0.12702,0.02228, 0.02015,
                0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                0.00978, 0.0236, 0.0015, 0.01974, 0.00074]
    else:
        print('Error(get_language_freq): unsupported language')
        return []
    
'______________________________________________________________________________'

def file_to_text(filename):
    """
    ----------------------------------------------------
    Parameters:   filename (str)
    Return:       contents (str)
    Description:  Utility function to read contents of a file
                  Can be used to read plaintext or ciphertext
    Asserts:      filename is a valid name
    ---------------------------------------------------
    """
    assert is_valid_filename(filename), 'invalid filename'
    infile = open(filename,'r')
    contents = infile.read()
    infile.close()
    return contents

'______________________________________________________________________________'

def text_to_file(text, filename):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  filename (str)            
    Return:       no returns
    Description:  Utility function to write any given text to a file
                  If file already exist, previous contents will be erased
    Asserts:      text is a string and filename is a valid filename
    ---------------------------------------------------
    """
    assert type(text) == str , 'invalid text'
    assert is_valid_filename(filename), 'invalid filename'
    outfile = open(filename,'w')
    outfile.write(text)
    outfile.close()
    return

'______________________________________________________________________________'

def is_valid_filename(filename):
    """
    ----------------------------------------------------
    Parameters:   filename (str)
    Return:       True/False
    Description:  Checks if given input is a valid filename 
                  a filename should have at least 3 characters
                  and contains a single dot that is not the first or last character
    ---------------------------------------------------
    """
    if type(filename) != str:
        return False
    if len(filename) < 3:
        return False
    if '.' not in filename:
        return False
    if filename[0] == '.' or filename[-1] == '.':
        return False
    if filename.count('.') != 1:
        return False
    return True

'______________________________________________________________________________'
   
def load_dictionary(dict_file=None):
    """
    ----------------------------------------------------
    Parameters:   dict_file (str): filename
                        default value = None
    Return:       dict_list (list): 2D list
    Description:  Reads a given dictionary file
                  dictionary is assumed to be formatted as each word in a separate line
                  Returns a list of lists, list 0 contains all words starting with 'a'
                  list 1 all words starting with 'b' and so forth.
                  if no parameter given, use default file (DICT_FILE)
    Errors:       if invalid filename, print error msg, return []
    ---------------------------------------------------
    """
    if dict_file == None:
        dict_file = DICT_FILE
        
    if not is_valid_filename(dict_file):
        print('Error(load_dictionary): invalid filename')
        return []
    
    alphabet = get_base('lower')
    infile = open(dict_file, 'r',encoding=" ISO-8859-15") 
    dict_words = infile.readlines()
    dict_list = [[] for _ in range(26)]
    for w in dict_words:
        word = w.strip('\n')
        dict_list[alphabet.index(word[0])]+=[word]
    infile.close()
    return dict_list

'______________________________________________________________________________'

def text_to_words(text):
    """
    ----------------------------------------------------
    Parameters:   text (str)
    Return:       word_list (list)
    Description:  Reads a given text
                  Returns a list of strings, each pertaining to a word in the text
                  Words are separated by a white space (space, tab or newline)
                  Gets rid of all special characters at the start and at the end
    Asserts:      text is a string
    ---------------------------------------------------
    """
    assert type(text) == str, 'invalid input'
    special = get_base('special')
    word_list = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip('\n')
        line = line.split(' ')
        for i in range(len(line)):
            if line[i] != '':
                line[i] = line[i].strip(special)
                word_list+=[line[i]]
    return word_list

'______________________________________________________________________________'

def analyze_text(text, dict_list):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  dict_list (list)
    Return:       matches (int)
                  mismatches (int)
    Description:  Reads a given text, checks if each word appears in given dictionary
                  Returns number of matches and mismatches.
                  Words are compared in lowercase
                  Assumes a proper dict_list
    Asserts:      text is a string and dict_list is a list
    ---------------------------------------------------
    """
    assert type(text) == str and type(dict_list) == list, 'invalid input'
    word_list = text_to_words(text)
    alphabet = get_base('lower')
    match = 0
    mismatch = 0
    for w in word_list:
        if w.isalpha():
            list_num = alphabet.index(w[0].lower())
            if w.lower() in dict_list[list_num]:
                match+=1
            else:
                mismatch+=1
        else:
            mismatch+=1
    return match,mismatch

'______________________________________________________________________________'

def is_plaintext(text, dict_list, threshold=0.9):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  dict_list (list): dictionary list
                  threshold (float): number between 0 to 1
                      default value = 0.9
    Return:       True/False
    Description:  Check if a given file is a plaintext
                  If #matches/#words >= threshold --> True
                      otherwise --> False
                  If invalid threshold, set to default value of 0.9
                  An empty text should return False
                  Assumes a valid dict_list is passed
    ---------------------------------------------------
    """
    if text == '':
        return False
    
    result = analyze_text(text, dict_list)
    
    percentage = result[0]/(result[0]+result[1])
    
    if type(threshold) != float or threshold < 0 or threshold > 1:
        threshold = 0.9 
    
    if percentage >= threshold:
        return True
    return False

'______________________________________________________________________________'

def new_matrix(r,c,fill):
    """
    ----------------------------------------------------
    Parameters:   r: #rows (int)
                  c: #columns (int)
                  fill (str,int,double)
    Return:       matrix (2D List)
    Description:  Create an empty matrix of size r x c
                  All elements initialized to fill
                  minimum #rows and #columns = 2
                  If invalid value given, set to 2
    ---------------------------------------------------
    """
    r = r if r >= 2 else 2
    c = c if c>=2 else 2
    return [[fill] * c for _ in range(r)]

'______________________________________________________________________________'

def print_matrix(matrix):
    """
    ----------------------------------------------------
    Parameters:   matrix (2D List)
    Return:       -
    Description:  prints a matrix each row in a separate line
                  items separated by a tab
                  Assumes given parameter is a valid matrix
    ---------------------------------------------------
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j],end='\t')
        print()
    return

'______________________________________________________________________________'

def index_2d(input_list,item):
    """
    ----------------------------------------------------
    Parameters:   input_list (list): 2D list
                  item (?)
    Return:       i (int): row number
                  j (int): column number
    Description:  Performs linear search on input list to find "item"
                  returns i,j, where i is the row number and j is the column number
                  if not found returns -1,-1
    Asserts:      input_list is a list
    ---------------------------------------------------
    """
    assert type(input_list) == list, 'invalid input'
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if input_list[i][j] == item:
                return i,j
    return -1,-1
'______________________________________________________________________________'

def shift_string(s,n,d='l'):
    """
    ----------------------------------------------------
    Parameters:   text (string): input string
                  shifts (int): number of shifts
                  direction (str): 'l' or 'r'
    Return:       update_text (str)
    Description:  Shift a given string by given number of shifts (circular shift)
                  If shifts is a negative value, direction is changed
                  If no direction is given or if it is not 'l' or 'r' set to 'l'
    Asserts:      text is a string and shifts is an integer
    ---------------------------------------------------
    """
    assert type(s) == str and type(n) == int
    if d != 'r' and d!= 'l':
        d = 'l'
    if n < 0:
        n = n*-1
        d = 'l' if d == 'r' else 'r'
    n = n%len(s)
    if s == '' or n == 0:
        return s

    s = s[n:]+s[:n] if d == 'l' else s[-1*n:] + s[:-1*n]
    return s

'______________________________________________________________________________'

def matrix_to_string(matrix):
    """
    ----------------------------------------------------
    Parameters:   matrix (2D List)
    Return:       text (string)
    Description:  convert a 2D list of characters to a string
                  from top-left to right-bottom
                  Assumes given matrix is a valid 2D character list
    ---------------------------------------------------
    """
    text = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            text+=matrix[i][j]
    return text

'______________________________________________________________________________'

def get_positions(text,base):
    """
    ----------------------------------------------------
    Parameters:   text (str): input string
                  base (str):  stream of unique characters
    Return:       positions (2D list)
    Description:  Analyzes a given text for any occurrence of base characters
                  Returns a 2D list with characters and their respective positions
                  format: [[char1,pos1], [char2,pos2],...]
                  Example: get_positions('I have 3 cents.','c.h') -->
                      [['h',2],['c',9],['.',14]]
                  items are ordered based on their occurrence in the text
    Asserts:      text and base are strings
    ---------------------------------------------------
    """
    assert type(text) == str and type(base) == str, 'invalid input'
    positions = []
    for i in range(len(text)):
        if text[i] in base:
            positions.append([text[i],i])
    return positions

'______________________________________________________________________________'

def clean_text(text,base):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  base (str)
    Return:       updated_text (str)
    Description:  Constructs and returns a new text which has
                  all characters in original text after removing base characters
    Asserts:      text and base are strings
    ---------------------------------------------------
    """
    assert type(text) == str and type(base) == str, 'invalid input'
    updated_text = ''
    for char in text:
        if char not in base:
            updated_text += char
    return updated_text

'______________________________________________________________________________'

def insert_positions(text, positions):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  positions (list): [[char1,pos1],[char2,pos2],...]]
    Return:       updated_text (str)
    Description:  Inserts all characters in the positions 2D list (generated by get_positions)
                  into their respective locations
                  Assumes a valid positions 2d list is given
    Asserts:      text is a string and positions is a list
    ---------------------------------------------------
    """
    assert type(text) == str and type(positions) == list, 'invalid input'
    updated_text = text
    for item in positions:
        updated_text = updated_text[:item[1]]+ item[0] + updated_text[item[1]:]
    return updated_text

'______________________________________________________________________________'

def text_to_blocks(text,b_size,padding = False,pad =PAD):
    """
    ----------------------------------------------------
    Parameters:   text (str): input string
                  block_size (int)
                  padding (bool): False(default) = no padding, True = padding
                  pad (str): padding character, default = PAD
    Return:       blocks (list)
    Description:  Create a list containing strings each of given block size
                  if padding flag is set, pad empty blocks using given padding character
                  if no padding character given, use global PAD
    Asserts:      text is a string and block_size is a positive integer
    ---------------------------------------------------
    """
    assert type(text) == str and type(b_size) == int and b_size > 0, 'invalid input'
    
    blocks = [text[i*b_size:(i+1)*b_size] for i in range(ceil(len(text)/b_size))]
    
    if padding:
        if (len(blocks) == 1 and len(blocks[0] < b_size)) or \
            len(blocks) > 1 and len(blocks[-1]) < len(blocks[0]):
                blocks[-1] += pad*(b_size - len(blocks[-1]))
    
    return blocks

'______________________________________________________________________________'

def blocks_to_baskets(blocks):
    """
    ----------------------------------------------------
    Parameters:   blocks (list): list of equal size strings
    Return:       baskets: (list): list of equal size strings
    Description:  Create k baskets, where k = block_size
                  basket[i] contains the ith character from each block
    Errors:       if blocks are not strings or are of different sizes -->
                    print 'Error(blocks_to_baskets): invalid blocks', return []
    ----------------------------------------------------
    """
    valid_input = True
    if type(blocks) != list or list == []:
        valid_input = False
    else:
        for b in blocks:
            if type(b) != str:
                valid_input = False
                break
        if valid_input:
            n = len(blocks[0])
            for b in blocks:
                if len(b) != n:
                    valid_input = False
                    break
    
    baskets = []
    if valid_input:      
        n = len(blocks[0])
        for j in range(n):
            basket = ''
            for i in range(len(blocks)):
                if j < len(blocks[i]):
                    basket+=blocks[i][j]
            baskets.append(basket)
    else:
        print('Error(blocks_to_baskets): invalid blocks')
    return baskets

'______________________________________________________________________________'

def compare_texts(text1,text2):
    """
    ----------------------------------------------------
    Parameters:   text1 (str)
                  text2 (str)
    Return:       matches (int)
    Description:  Compares two strings and returns number of matches
                  Comparison is done over character by character
    Assert:       text1 and text2 are strings
    ----------------------------------------------------
    """
    assert type(text1) == str and type(text2) == str, 'invalid input'
    counter = 0
    matches = 0
    while counter < len(text1) and counter <len(text2):
        if text1[counter] == text2[counter]:
            matches += 1
        counter +=1
    return matches

'______________________________________________________________________________'

def get_freq(text,base = ''):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  base (str): default = ''
    Return:       count_list (list of floats) 
    Description:  Finds character frequencies (count) in a given text
                  Default is English language (counts both upper and lower case)
                  Otherwise returns frequencies of characters defined in base
    Assert:       text is a string
    ----------------------------------------------------
    """
    assert type(text) == str , 'invalid input'
    if base == None:        
        return [text.count(chr(97+i))+text.count(chr(65+i)) for i in range(26)]
    return [text.count(char) for char in base]

'______________________________________________________________________________'

def is_binary(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       True/False
    Description:  Checks if given input is a string that represent a valid
                  binary number
                  An empty string, or a string that contains other than 0 or 1
                  should return False
    ---------------------------------------------------
    """
    if type(b) != str or b == '':
        return False
    for i in range(len(b)):
        if b[i]!= '0' and b[i]!='1':
            return False
    return True

'______________________________________________________________________________'

def bin_to_dec(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       decimal (int)
    Description:  Converts a binary number into corresponding integer
    Errors:       if not a valid binary number: 
                      print 'Error(bin_to_dec): invalid input' and return empty string
    ---------------------------------------------------
    """
    if not is_binary(b):
        print('Error(bin_to_dec): invalid input')
        return ''
    value = 0
    exponent = len(b)-1
    for i in range(len(b)):
        if b[i] == '1':
            value+= 2**exponent
        exponent-=1
    return value

'______________________________________________________________________________'

def dec_to_bin(decimal,size=None):
    """
    ----------------------------------------------------
    Parameters:   decimal (int): input decimal number
                  size (int): number of bits in output binary number
                      default size = None
    Return:       binary (str): output binary number
    Description:  Converts any integer to binary
                  Result is to be represented in size bits
                  pre-pad with 0's to fit the output in the given size
                  If no size is given, no padding is done 
    Asserts:      decimal is an integer
    Errors:       if an invalid size:
                      print 'Error(dec_to_bin): invalid size' and return ''
                  if size is too small to fit output binary number:
                      print 'Error(dec_to_bin): integer overflow' and return ''
    ---------------------------------------------------
    """
    assert type(decimal) == int, 'invalid input'
    
    if (size != None and type(size) != int) or (type(size) == int and size <1):
        print('Error(dec_to_bin): invalid size')
        return ''
    
    binary = ''
    q = 1
    r = 0
    while q!=0:
        q = decimal//2
        r = decimal%2
        decimal = q
        binary = str(r)+binary
    
    if size == None:
        return binary
    
    if len(binary) > size:
        print('Error(dec_to_bin): integer overflow')
        return ''
    
    while len(binary)!= size:
        binary = '0'+binary
    return binary

'______________________________________________________________________________'

def xor(a,b):
    """
    ----------------------------------------------------
    Parameters:   a (str): binary number
                  b (str): binary number
    Return:       decimal (int)
    Description:  Apply xor operation on a and b
    Errors:       if a or b is not a valid binary number 
                      print 'Error(xor): invalid input' and return ''
                  if a and b have different lengths:
                       print 'Error(xor): size mismatch' and return ''
    ---------------------------------------------------
    """
    if not is_binary(a) or not is_binary(b):
        print('Error(xor): invalid input')
        return ''
    if len(a)!= len(b):
        print('Error(xor): size mismatch')
        return ''
    c = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            c+='0'
        else:
            c+='1'
    return c

'______________________________________________________________________________'

def encode(c,code_type):
    """
    ----------------------------------------------------
    Parameters:   c (str): a character
                  code_type (str): ASCII or B6
    Return:       b (str): corresponding binary number
    Description:  Encodes a given character using the given encoding scheme
                  Current implementation supports only ASCII and B6 encoding
    Errors:       If c is not a single character:
                    print 'Error(encode): invalid input' and return ''
                  If unsupported encoding type:
                    print 'Error(encode): Unsupported Coding Type' and return ''
    ---------------------------------------------------
    """
    if not isinstance(c,str) or len(c)!=1:
        print('Error(encode): invalid input')
        return ''
    if code_type == 'B6':
        return _encode_B6(c)
    elif code_type == 'ASCII':
        return dec_to_bin(ord(c),8)
    else:
        print('Error(encode): Unsupported coding type')
        return ''

def _encode_B6(c):
    """
    ----------------------------------------------------
    Parameters:   c (str): a character
    Return:       B6_code (str): 6-digit binary code
    Description:  Encodes any given symbol in the B6 Encoding scheme
                  If given symbol is one of the 64 symbols
                  return binary representation, which is the binary representation
                  of the position of the symbol in the B6 base
                  If the given symbol is not part of the B6Code --> 
                        return empty string (no error msg)
    Error:        If given input is not a single character -->
                      print 'Error(encode_B6): invalid input' and return ''
    ---------------------------------------------------
    """
    if not isinstance(c,str) or len(c)!= 1:
        print('Error(encode_B6): invalid input')
        return ''
    code = get_base('B6')
    if c not in code:
        return ''
    indx = code.index(c)
    return dec_to_bin(indx,6)

'______________________________________________________________________________'

def decode(b,code_type):
    """
    ----------------------------------------------------
    Parameters:   b (str): a binary number
                  code_type (str): ASCII or B6
    Return:       c (str): corresponding character
    Description:  Encodes a given character using the given encoding scheme
                  Current implementation supports only ASCII and B6 encoding
    Errors:       If b is not a binary number:
                    print 'Error(decode): invalid input' and return ''
                  If unsupported encoding type:
                    print 'Error(decode): unsupported Coding Type' and return ''
    ---------------------------------------------------
    """
    if not is_binary(b):
        print('Error(decode): invalid input')
        return ''
    if code_type == 'B6':
        return _decode_B6(b)
    elif code_type == 'ASCII':
        return chr(bin_to_dec(b))
    else:
        print('Error(decode): unsupported coding type')
        return ''

def _decode_B6(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       c (str): a character
    Description:  Decodes any given binary code in the B6 Coding scheme
    Errors:       If given input is not a valid 6-bit binary number -->
                      print 'Error(decode_B6): invalid input
                      return empty string
    ---------------------------------------------------
    """
    if not isinstance(b,str) or len(b)!=6 or not is_binary(b):
        print('Error(decode_B6): invalid input')
        return ''
    value = bin_to_dec(b)
    B6Code = get_base('B6')
    return B6Code[value]

