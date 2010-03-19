# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the file locator returns the correct location tag
"""


def test():
    import pyre.tracking

    locator = pyre.tracking.newFileLocator(source="script.py", line=16, column=2)

    assert str(locator) == "file='script.py', line=16, column=2"

    return locator


# main
if __name__ == "__main__":
    test()


# end of file 
