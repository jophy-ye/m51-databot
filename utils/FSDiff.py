"""
FSDiff.py contains the FSDiff class.

If a dir is given to FSDiff, it monitors the changes of files within the dir and returns a list of (filename, tag)
tuples. A valid tag can only be NEW (0), MODIFIED (1), DELETED (2), signaling the difference of a file.
"""
