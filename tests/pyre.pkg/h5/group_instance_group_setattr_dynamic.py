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

    # make a group with some data
    class Meta(pyre.h5.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.bool()
        flag.default = True
        flag.pyre_doc = "a boolean"

    # embed it in another group
    class Group(pyre.h5.group):
        """
        A group that contains a subgroup
        """

        # the subgroup
        meta = Meta()

    # build a descriptor for a dynamic group
    data = pyre.h5.group(name="data")
    # and a dynamic dataset
    HH = pyre.h5.bool(name="HH", default=True)

    # instantiate
    g = Group()
    # attach the new group
    g.pyre_extend(identifier=data)

    # verify that we get the exact same object every time we ask for the new identifier
    assert g.data is g.data

    # and the dataset to the new group
    g.data.pyre_extend(identifier=HH)
    # check that we pick up the default value
    assert g.data.HH.value == True
    # that we can change it
    g.data.HH.value = False
    # and it sticks
    assert g.data.HH.value == False

    # to check that the identifier is involved in the assignment
    try:
        # try something that should fail to convert to bool
        g.data.HH.value = 5
        # we shouldn't be able to reach here
        assert False
    # if the correct exception is raised
    except pyre.schemata.exceptions.CastingError:
        # we are all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
