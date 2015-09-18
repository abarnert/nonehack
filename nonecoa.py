import collections
import importlib
import importlib.machinery
import io
import itertools
from itertools import chain
import pprint
import sys
from tokenize import * #tokenize, untokenize, ERRORTOKEN, NAME, OP
            
def _call_with_frames_removed(f, *args, **kwargs):
    return f(*args, **kwargs)

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)

def groupwise_longest(iterable, n):
    bits = itertools.tee(iterable, n)
    for i, bit in enumerate(bits):
        consume(bit, i)
    return itertools.zip_longest(*bits)

def retokenize(tokens):
    """Coalesce None.

       Replace:
       
         name?.attr
          
       with:
        
         name.attr if name is not None else None
    """
    # See http://bugs.python.org/issue16224#msg211469
    # "Switching from 5-tuples to 2-tuples... is not currently a
    # supported use case". In particular, if you do so in the middle
    # of an indented block, the dedent doesn't match the indent. So,
    # we have to force everything to 2-tuples.    
    groups = groupwise_longest(tokens, 4)
    for w, x, y, z in groups:
        if (w[0] == NAME and z is not None and
            x[0] == ERRORTOKEN and x[1] == '?' and
            y[0] == OP and y[1] == '.'):
            yield w[0], w[1]
            yield y[0], y[1]
            yield z[0], z[1]
            yield NAME, 'if'
            yield w[0], w[1]
            yield NAME, 'is'
            yield NAME, 'not'
            yield NAME, 'None'
            yield NAME, 'else'
            yield NAME, 'None'
            consume(groups, 3)
        else:
            yield w[0], w[1]

class NoneCoaLoader(importlib.machinery.SourceFileLoader):
    def source_to_code(self, data, path, *, _optimize=-1):
        print(path)
        source = importlib._bootstrap.decode_source(data)
        tokens = tokenize(io.BytesIO(source.encode('utf-8')).readline)
        tokens = retokenize(tokens)
        source = untokenize(tokens).decode('utf-8')
        return _call_with_frames_removed(compile, source, path, 'exec',
                                         dont_inherit=True,
                                         optimize=_optimize)

_real_pathfinder = sys.meta_path[-1]

class NoneCoaFinder(type(_real_pathfinder)):
    @classmethod
    def find_module(cls, fullname, path=None):
        spec = _real_pathfinder.find_spec(fullname, path)
        if not spec: return spec
        loader = spec.loader
        if type(loader).__name__ == 'SourceFileLoader':
            loader.__class__ = NoneCoaLoader
        return loader

sys.meta_path[-1] = NoneCoaFinder
