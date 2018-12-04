import random
import string

def secret_key(length=10):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))#.upper()