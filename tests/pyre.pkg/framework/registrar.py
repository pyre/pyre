#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercises the component registrar
"""


def test():
    import pyre

    # build the executive
    executive = pyre.executive

    # access the component registrar
    assert executive.registrar is not None

    # all done
    return executive


# main
if __name__ == "__main__":
    test()


# end of file
