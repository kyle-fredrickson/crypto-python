#!/usr/bin/python3

import os
import sys
import traceback
from Crypto.Cipher import DES

import des

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TEST_VECTORS = os.path.abspath(os.path.join(THIS_DIR, "test_vectors.txt"))

def test(test_vector):
    errors = []

    key = test_vector["key"]
    plain = test_vector["plain"]
    cipher = test_vector["cipher"]

    my_encrypted_block = des.encrypt(plain, key)
    my_decrypted_block = des.decrypt(my_encrypted_block, key)

    key_bytes = key.to_bytes(8, byteorder='big')
    plain_bytes = plain.to_bytes(8, byteorder='big')
    other_DES = DES.new(key_bytes, DES.MODE_ECB)

    other_encrypted_block = int.from_bytes(other_DES.encrypt(plain_bytes), 'big')

    if (my_decrypted_block != plain):
        errors.append("Error: decryption failed at line %d." % test_vector["line"])
    if (my_encrypted_block != cipher):
        errors.append("Error: failed test at line %d." % test_vector["line"])
    if (my_encrypted_block != other_encrypted_block):
        errors.append("Error: implementations disagree in test at line %d." % test_vector["line"])

    return errors

def parse_test_vectors(lines):
    tests = [{}] * (len(lines) - 1)
    for i in range(1, len(lines)):
        [key, plain, cipher] = lines[i].split("\t")
        tests[i - 1] = {"line": i + 1, "key": int(key, 16), "plain": int(plain, 16), "cipher": int(cipher, 16)}

    return tests

def main():
    errors = []

    try:
        with open(TEST_VECTORS, "r") as tests:
            test_vectors = parse_test_vectors(tests.read().splitlines())

        for test_vector in test_vectors:
            errors += test(test_vector)
    except Exception as ex:
        errors.append("Caught exception while testing: " + str(ex))
        print(traceback.format_exc())

    if len(errors) > 0:
        print("Errors occurred while testing.")
        for error in errors:
            print(" - " + error)
        sys.exit(1)
    else:
        print("All tests passed!")

if __name__ == "__main__":
    main()