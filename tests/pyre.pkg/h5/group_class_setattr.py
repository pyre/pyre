#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Exercise assignments to class attributes
"""


# the driver
def test():
    # support
    import pyre

    # make a group
    class Group(pyre.h5.group):
        """
        A group of datasets in some HDF5 file
        """

        # something simple
        id = pyre.h5.int()
        id.pyre_doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.list()
        pols.pyre_doc = "a dataset that's a container"

    # boring class attribute assignment
    Group.boring = True
    # verify it stuck
    assert Group.boring

    # assignment that modifies the default value of a known identifier
    # set up a value
    pols = ["HH", "HV", "VH", "VV"]
    # update the identifier
    Group.pols = pols
    # verify, but access carefully
    assert Group.pyre_identifiers["pols"].default == pols

    # assignment that adds a new identifier to the class
    # the identifier name
    name = "freq"
    # set up a default value
    freq = ["A", "B"]
    # add the identifier
    Group.freq = pyre.h5.list(name=name, default=freq)
    # verify that it's there
    freqId = Group.pyre_identifiers["freq"]
    # it picked up the name and location
    assert freqId.pyre_name == name
    assert freqId.pyre_location == pyre.primitives.path(name)
    # its type is correct
    assert freqId.typename == "list"
    # and its default value is what we expect
    assert freqId.default == freq

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
