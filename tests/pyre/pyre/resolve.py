#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise component resolution
"""


def test():
    # access the framework
    import pyre

    # resolve a trivial component
    c = pyre.resolve(uri='import:pyre.component')
    # check it
    assert c is pyre.component

    # something a bit more difficult
    t = pyre.resolve(uri='file:sample.py/worker#joe')
    # check it
    assert isinstance(t, pyre.component)
    assert t.pyre_name == 'joe'

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
