import collections
Point = collections.namedtuple('Point', 'x y')

def test():
    spam = Point(2, 3)
    print(spam.x)
    print(spam?.x)
    try:
        print(spam?.z)
    except AttributeError as e:
        print(repr(e))

    eggs = None
    try:
        print(eggs.x)
    except AttributeError as e:
        print(repr(e))
    print(eggs?.x)
    print(eggs?.z)

    try:
        print(None.x)
    except AttributeError as e:
        print(repr(e))        
    print(None?.x)
    print(None?.z)
