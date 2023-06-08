from sdes import SBOX, SDES, PRNG


def test_PRNG():
    print('{}'.format('-' * 40))
    print("Start of PRNG Testing")
    print()

    print('Testing Blum Blum Shub: ')
    p = [383, 11, 27691, 383, 383, 384]
    q = [503, 19, 11, 503, 503.0, 503]
    bits = [8, 4, 16, 0, 1, 1]
    for i in range(len(p)):
        output = PRNG.BBS(p[i], q[i], bits[i])
        print('PRNG.BBS({},{},{}) = {}'.format(p[i], q[i], bits[i], output))
    print()

    print('End of PRNG Testing')
    print('{}'.format('-' * 40))
    print()
    return


def test_sbox():
    print('{}'.format('-' * 40))
    print("Start of SBOX class testing")
    print()

    print('Creating an empty SBOX:')
    sbox = SBOX()
    print(sbox)
    print('sbox.substitute(1000) = {}'.format(sbox.substitute('1000')))
    print('sbox.is_empty() = {}'.format(sbox.is_empty()))
    print('sbox.get_size() = {}'.format(sbox.get_size()))
    print('sbox.get_box() = {}'.format(sbox.get_box()))
    print()

    print('Loading sbox1.txt:')
    print("sbox.set_box('sbox1.txt'): ", end='')
    print(sbox.set_box('sbox1.txt'))
    print(sbox)
    print('sbox.is_empty() = {}'.format(sbox.is_empty()))
    print('sbox.get_size() = {}'.format(sbox.get_size()))
    print('sbox.get_box() = {}'.format(sbox.get_box()))
    cases = ['1101', '0010', '0111', '0000', '010', 1010]
    for c in cases:
        print('sbox.substitute({}) = {}'.format(c, sbox.substitute(c)))
    print()

    print("sbox.set_box('sbox2.txt'): ", end='')
    print(sbox.set_box('sbox2.txt'))
    print(sbox)
    cases = ['1101', '0010', '0111', '0000', '010', 1010]
    for c in cases:
        print('sbox.substitute({}) = {}'.format(c, sbox.substitute(c)))
    print()

    print('End of SBOX class Testing')
    print('{}'.format('-' * 40))
    print()
    return


def test_sdes_basics():
    print('{}'.format('-' * 40))
    print("Start of SDES basics testing")
    print()

    sdes = SDES()
    print('Testing default values (get_value):')
    cases = ['rounds', 'key_length', 'block_size', 'encoding', 'sbox1',
             'sbox2', 'p', 'q', 'pad']
    for c in cases:
        print('sdes.get_value({}) = {}'.format(c, sdes.get_value(c)))
    print('sdes.get_value(size) = ', end='')
    sdes.get_value('size')
    print()

    cases = [['rounds', 5], ['rounds', 1], ['rounds', 4.3],
             ['p', 683], ['p', 899],
             ['q', 684], ['q', 13.2],
             ['pad', 'r'], ['pad', 'ab'], ['pad', 1], ['pad', '?'],
             ['encoding', 'B6'], ['encoding', 'ascii'],
             ['block_size', 1024], ['block_size', 243], ['block_size', 512.0],
             ['key_length', 64],
             ['sbox_size', 128]]
    print('Testing set_parameter:')
    for c in cases:
        print('sdes.set_parameter({},{}) = {}'.format(c[0], c[1], sdes.set_parameter(c[0], c[1])))
    print()

    print('End of SDES basics Testing')
    print('{}'.format('-' * 40))
    print()
    return


def test_sdes_keys():
    print('{}'.format('-' * 40))
    print("Start of SDES keys testing")
    print()

    print('Testing get_key:')
    sdes = SDES()
    print('p = {}, q = {}'.format(sdes.get_value('p'), sdes.get_value('q')))
    print('sdes.get_key() = {}'.format(sdes.get_key()))
    sdes.set_parameter('p', 683)
    print('p = {}, q = {}'.format(sdes.get_value('p'), sdes.get_value('q')))
    print('sdes.get_key() = {}'.format(sdes.get_key()))
    sdes.set_parameter('q', 503)
    print('p = {}, q = {}'.format(sdes.get_value('p'), sdes.get_value('q')))
    print('sdes.get_key() = {}'.format(sdes.get_key()))
    print()

    print('Testing get_subkey:')
    print('key = {}'.format(sdes.get_key()))
    for i in range(12):
        print('subkey({}) = {}'.format(i, sdes.get_subkey(i)))
    print()

    print('End of SDES keys Testing')
    print('{}'.format('-' * 40))
    print()
    return


def test_feistel():
    print('{}'.format('-' * 40))
    print("Start of Feistel Network testing")
    print()

    sdes = SDES()

    print('Testing expand:')
    cases = ['011001', '00001111', '0011', '', 1011]
    for c in cases:
        print('sdes.expand({}) = {}'.format(c, sdes.expand(c)))
    print()

    print('Testing F function:')
    bi = ['111000', '100110', '10011', '100110']
    ki = ['00011010', '01100101', '01100101', '0110010']
    for i in range(len(bi)):
        print('F({},{}) = {}'.format(bi[i], ki[i], sdes.F(bi[i], ki[i])))
    print()

    print('Testing feistel:')
    bi = ['011100100110', '010001100101', '01110010011', '011100100110']
    ki = ['01100101', '11000001', '01100101', '0110010']
    for i in range(len(bi)):
        print('feistel({},{}) = {}'.format(bi[i], ki[i], sdes.feistel(bi[i], ki[i])))
    print()

    print('End of Feistel Network Testing')
    print('{}'.format('-' * 40))
    print()
    return


def test_ECB():
    print('{}'.format('-' * 40))
    print("Start of SDES ECB Mode testing")
    print()

    sdes = SDES()

    p = [11, 503, 27691, 683, 19, 27691]
    q = [19, 23, 11, 503, 59, 23]
    pads = ['q', 'x', 'Q', 'q', '.', 'X']
    rounds = [2, 3, 4, 2, 3, 2]
    plaintexts = ['OK', 'Sit', 'beet', 'welcome',
                  '"Cryptography" is power', 'go-go']
    for i in range(len(plaintexts)):
        sdes.set_parameter('p', p[i])
        sdes.set_parameter('q', q[i])
        sdes.set_parameter('pad', pads[i])
        sdes.set_parameter('rounds', rounds[i])
        print('key = {}'.format(sdes.get_key()))
        plaintext = plaintexts[i]
        print('plaintext  = {}'.format(plaintext))
        ciphertext = sdes.encrypt(plaintext, 'ECB')
        print('ciphertext = {}'.format(ciphertext))
        plaintext2 = sdes.decrypt(ciphertext, 'ECB')
        print('plaintext2 = {}'.format(plaintext2))
        print()

    print('End of SDES ECB Mode Testing')
    print('{}'.format('-' * 40))
    print()
    return


def test_CBC():
    print('{}'.format('-' * 40))
    print("Start of SDES CBC Mode testing")
    print()

    sdes = SDES()

    p = [11, 43, 27691, 683, 43]
    q = [19, 23, 11, 503, 683]
    plaintexts = ['go', 'CAT', 'seed', 'go-go', 'cryptanalysis tricks']
    for i in range(len(plaintexts)):
        sdes.set_parameter('p', p[i])
        sdes.set_parameter('q', q[i])
        print('key = {}'.format(sdes.get_key()))
        plaintext = plaintexts[i]
        print('plaintext  = {}'.format(plaintext))
        ciphertext = sdes.encrypt(plaintext, 'CBC')
        print('ciphertext = {}'.format(ciphertext))
        plaintext2 = sdes.decrypt(ciphertext, 'CBC')
        print('plaintext2 = {}'.format(plaintext2))
        print()

    print('End of SDES CBC Mode Testing')
    print('{}'.format('-' * 40))
    print()
    return


test_PRNG()
test_sbox()
test_sdes_basics()
test_sdes_keys()
test_feistel()
test_ECB()
test_CBC()
