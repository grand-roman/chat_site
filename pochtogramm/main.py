from functools import wraps


def wrapper(func):
    @wraps(func)
    def wrapped(first_argument, *args, **kwargs):
        print(f'calling {func.__name__}')
        print(first_argument)
        res = func("asdf", *args, **kwargs)
        print(f'finished {func.__name__}')
        return res
    return wrapped


@wrapper
def provider(name: str):
    counter = 0
    print(f"{name}: {counter}")
    def fasdfasdf():
        nonlocal counter
        print(f"{name}: {counter}")
        counter += 1
    return fasdfasdf


provider("f1")

# print(f'calling {ff.__name__}')

