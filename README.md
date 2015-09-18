# nonehack
A quick hack to add None coalescing syntax to Python

The usual caveats for playing with quick&dirty import hacks apply. In particular:
 * You must have a main script that does an `import nonecoahack` and then imports
your real main code as a module. (See `nonecoa.py` and `nonecoatest.py` if this
isn't clear.)
 * If you want to hack on the hack itself, you generally need
to `touch *.py` or `rm -rf __pycache__` to make sure the changes take effect.
 * Tracebacks, etc. may be ugly.
 * Do not use with any other import hooks, including non-hacky ones.
