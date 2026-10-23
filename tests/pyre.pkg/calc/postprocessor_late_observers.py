#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the nodes that depend on a node follow it when it acquires a postprocessor after
they have read its value
"""


def test():
    """
    Build a node from text and a node that refers to it, read both, then give the first one a
    postprocessor and check that the second one sees the converted value
    """
    # access the package
    import pyre.calc

    # set up the model
    model = pyre.calc.model()
    # make a node that holds text, the way the configuration store gets it
    count = model.variable(value="0x10")
    # register it
    model["count"] = count
    # make a node that refers to it
    label = model.interpolation(value="{count} items")
    # and register it too
    model["label"] = label

    # read the dependent, which reads its referent as text
    assert label.value == "0x10 items"
    # both caches are current: the referent's
    assert count.dirty == False
    # and the dependent's
    assert label.dirty == False

    # give the referent a type
    count.postprocessor = hexadecimal
    # which invalidates its cache
    assert count.dirty == True
    # and the cache of the node that depends on it
    assert label.dirty == True
    # so the dependent sees the converted value
    assert label.value == "16 items"

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
