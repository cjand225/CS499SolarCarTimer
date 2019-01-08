import random, string


def randomWord(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
