import functools


def history_shoots(func):
    shoots = {}

    @functools.wraps(func)
    def inner(*args):
        location = args[1]
        if location in shoots:
            return shoots[location]
        else:
            res = func(*args)
            shoots[location] = res
            return res

    return inner
