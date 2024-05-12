import hashlib
import time


def number_sha256(number):
    byte_length = (number.bit_length() + 7) // 8
    byte_data = number.to_bytes(byte_length, byteorder='big')
    hash_object = hashlib.sha256()
    hash_object.update(byte_data)
    return hash_object.hexdigest()


def sha256(text):
    byte_data = text.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(byte_data)
    return hash_object.hexdigest()


def get_timestamp():
    return int(time.time())
