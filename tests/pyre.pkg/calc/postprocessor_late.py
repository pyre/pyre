#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a node acquires a postprocessor after it was built and read, and that its next
read goes through it
"""


def test():
    """
    Build a node from text, read it, attach a postprocessor, and read it again
    """
    # access the package
    import pyre.calc

    # set up the model
    model = pyre.calc.model()
    # make a node that holds text, the way the configuration store gets it
    count = model.variable(value="0x10")
    # register it
    model["count"] = count

    # read it before anybody has said what type it is
    assert count.value == "0x10"
    # which leaves its cache current
    assert count.dirty == False

    # now give it a type
    count.postprocessor = hexadecimal
    # which invalidates the cached text
    assert count.dirty == True
    # so the next read goes through the postprocessor
    assert count.value == 16
    # and caches the converted value
    assert count.dirty == False

    # all done
    return


def hexadecimal(value, **kwds) -> int:
    """
    Convert {value} to an integer, honoring its base prefix
    """
    # let python figure out the base from the prefix
    return int(value, 0)


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
