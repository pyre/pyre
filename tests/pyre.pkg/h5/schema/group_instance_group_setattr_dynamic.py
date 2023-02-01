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
    import journal
    import pyre

    # make a group with some data
    class Meta(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.schema.bool()
        flag.default = True
        flag.doc = "a boolean"

    # embed it in another group
    class Group(pyre.h5.schema.group):
        """
        A group that contains a subgroup
        """

        # the subgroup
        meta = Meta()

    # build a descriptor for a dynamic group
    data = pyre.h5.schema.group(name="data")
    # and a dynamic dataset
    HH = pyre.h5.schema.bool(name="HH", default=True)

    # instantiate
    g = Group(name="root")
    # attach the new group
    setattr(g, data._pyre_name, data)

    # verify that we get the exact same object every time we ask for the new identifier
    assert g.data is g.data

    # attach the dataset to the new group
    setattr(g.data, HH._pyre_name, HH)
    # check that we pick up the default value
    assert g.data.HH.default == True
    # that we can change its default value
    g.data.HH = False
    # and it sticks
    assert g.data.HH.default == False

    # to check that illegal assignments are trapped correctly
    try:
        # silence firewalls
        journal.firewall("pyre.h5.schema").device = journal.trash()
        # try assigning a group member that is not a descriptor
        g.data = 5
        # we shouldn't be able to reach here
        assert False
    # if the correct exception is raised
    except journal.FirewallError:
        # we are all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
