#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

"""
Exercise the important special case of building a path with a tuple as a single
argument. For example, this happens when paths are unpickled.
"""

def test():
    # the home of the path factory
    import pyre.primitives

    # make one
    c = pyre.primitives.path.cwd()
    # show me
    # print(c)
    # turn it into a tuple
    t = tuple(c)
    # show me
    # print(t)
    # use the tuple to build a path
    r = pyre.primitives.path(t)
    # show me
    # print(r)
    # check that they are identical; this checks whether all the representational decisions are
    # respected.
    assert c == r

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
