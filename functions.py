import random
import string
import base64 as b64
from hashlib import sha256


def generate_random_string(length):
    """
    Generates a random string of length characters (Code Verifier generator)
    :param length: length of the string
    :return: random string
    """
    possible = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.SystemRandom().choice(possible) for _ in range(length))


def sha256_hash(text):
    """
    Hashes a string using sha256
    :param text: string to be hashed
    :return:  string
    """
    return sha256(text.encode('ascii')).digest()


def base64_encoder(hashed):
    """
    Encodes a string using base64
    :param hashed: hashed to be encoded
    :return: string
    """
    encoded = b64.b64encode(hashed).decode('utf-8')
    return encoded.replace('=', '').replace('+', '-').replace('/', '_')
