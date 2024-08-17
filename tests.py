from AES import AES_256


def test_key_expansion():
    instance = AES_256()
    ret_w = instance.KeyExpansion(b'\x60\x3d\xeb\x10\x15\xca\x71\xbe\x2b\x73\xae\xf0\x85\x7d\x77\x81\x1f\x35\x2c\x07\x3b\x61\x08\xd7\x2d\x98\x10\xa3\x09\x14\xdf\xf4',b'\x00'*240, 8, 4, 14, verbose=False)
    actual_w = bytearray.fromhex('603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff49ba354118e6925afa51a8b5f2067fcdea8b09c1a93d194cdbe49846eb75d5b9ad59aecb85bf3c917fee94248de8ebe96b5a9328a2678a647983122292f6c79b3812c81addadf48ba24360af2fab8b46498c5bfc9bebd198e268c3ba709e0421468007bacb2df331696e939e46c518d80c814e20476a9fb8a5025c02d59c58239de1369676ccc5a71fa2563959674ee155886ca5d2e2f31d77e0af1fa27cf73c3749c47ab18501ddae2757e4f7401905acafaaae3e4d59b349adf6acebd10190dfe4890d1e6188d0b046df344706c631e')
    #Test if key expansion works as per https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf A.3 - Expansion of a 256-bit Cipher Key page 30
    assert(ret_w == actual_w)
    return True

def test_encrypt():
    instance = AES_256(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f')
    cipher = instance.Encrypt(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff', verbose = False)
    #Test if encryption works as per https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf C.3 AES-256 (Nk=8, Nr=14) page 42
    assert(cipher == b'\x8e\xa2\xb7\xca\x51\x67\x45\xbf\xea\xfc\x49\x90\x4b\x49\x60\x89')
    return True

def test_decrypt():
    instance = AES_256(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f')
    plaintext = instance.Decrypt(b'\x8e\xa2\xb7\xca\x51\x67\x45\xbf\xea\xfc\x49\x90\x4b\x49\x60\x89', verbose=False)
    #Test if decryption works as per https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf INVERSE CIPHER (DECRYPT): page 43
    assert(plaintext == b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff')
    return True

def test_decrypt_cyclic():
    instance = AES_256(b'ThisIsTheBestPasswordICanThinkOf')
    cipher = instance.Encrypt(b'Hello world!  :)', verbose=False)
    plaintext = instance.Decrypt(cipher, verbose=False)
    # Test if we encrypt data then decrypt it we should get the same plaintext out
    assert(plaintext == b'Hello world!  :)')
    return True

def test_gcm():
    instance = AES_256(b'ThisIsTheBestPasswordICanThinkOf')
    ciphertext, tag = instance.EncryptGCM(b'Hello world!  :)', verbose=False)
    plaintext, d_tag = instance.DecryptGCM(ciphertext, verbose=False)
    assert(plaintext == b'Hello world!  :)')
    assert(tag == d_tag)
    return True



assert(test_key_expansion())
assert(test_encrypt())
assert(test_decrypt())
assert(test_decrypt_cyclic())
assert(test_gcm())
print("All tests passed")