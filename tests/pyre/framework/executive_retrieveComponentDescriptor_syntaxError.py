#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that bad component descriptors raise the correct exceptions
"""


def test():
    import pyre.framework
    executive =  pyre.framework.executive()

    # retrieve a component descriptor from the python path
    try:
        executive.retrieveComponentDescriptor(uri="file:sample_syntaxerror.py/factory")
        assert False
    except SyntaxError as error:
        pass
    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file 
