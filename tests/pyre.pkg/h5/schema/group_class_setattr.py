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
    class Group(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something simple
        id = pyre.h5.schema.int()
        id.__doc__ = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.schema.list()
        pols.__doc__ = "a dataset that's a container"

    # boring class attribute assignment
    Group.boring = True
    # verify it stuck
    assert Group.boring

    # assignment that modifies the default value of a known descriptor
    # set up a value
    pols = ["HH", "HV", "VH", "VV"]
    # update the descriptor
    Group.pols = pols
    # verify, but access carefully
    assert Group._pyre_descriptors["pols"].default == pols

    # assignment that adds a new descriptor to the class
    # the descriptor name
    name = "freq"
    # set up a default value
    freq = ["A", "B"]
    # add the descriptor
    Group.freq = pyre.h5.schema.list(name=name, default=freq)
    # verify that it's there
    freqId = Group._pyre_descriptors["freq"]
    # it got bound to the correct name
    assert freqId._pyre_name == name
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
