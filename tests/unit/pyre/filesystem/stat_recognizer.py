#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that stat recognizers can be instantiated
"""


def test():
    import pyre.filesystem
    return pyre.filesystem.newStatRecognizer()


# main
if __name__ == "__main__":
    test()


# end of file 
