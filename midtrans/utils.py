import random
import string


def random_string_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_order_id():
    return random_string_generator(size=50)