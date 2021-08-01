import random
import string


def random_str(str_length):
    return ''.join(random.sample(string.ascii_letters + string.digits, str_length))