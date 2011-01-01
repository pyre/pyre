#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the file region locator returns the correct location tag
"""


def test():
    import pyre.tracking

    start = pyre.tracking.newFileLocator(source="script.py", line=16, column=2)
    end = pyre.tracking.newFileLocator(source="script.py", line=17, column=52)

    region = pyre.tracking.newFileRegionLocator(start=start, end=end)

    assert str(region) == "file='script.py', from (line=16, column=2) to (line=17, column=52)"

    return region


# main
if __name__ == "__main__":
    test()


# end of file 
