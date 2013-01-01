#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Sanity check: instantiate a weaver and verify its configuration
"""


def test():
    # get the package
    import pyre.weaver
    # instantiate a weaver
    weaver = pyre.weaver.newWeaver(name="sanity")
    # by default, there is no language setting
    assert weaver.language == None
    # and return it
    return weaver


# main
if __name__ == "__main__":
    test()


# end of file 
