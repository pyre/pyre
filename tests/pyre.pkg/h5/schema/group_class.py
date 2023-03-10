#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Check that we can harvest datasets from groups
"""


# the driver
def test():
    # support
    import journal
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
        pols = pyre.h5.schema.list(schema=pyre.h5.schema.int())
        pols.__doc__ = "a dataset that's a container"

    # verify that my table of descriptors is accessible
    descriptors = Group._pyre_classDescriptors
    # and of the correct size
    assert len(descriptors) == 2
    # check the contents
    assert getattr(Group, "id").typename == "int"
    assert getattr(Group, "pols").typename == "list"

    # configure the journal
    journal.application("pyre.h5.group")
    # make a channel
    channel = journal.debug("pyre.h5.group")

    # sign on
    channel.line(f"group: {Group.__name__}")

    # descriptor section
    channel.line(f"  descriptors:")
    # go through the contents of the descriptor map
    for name in Group._pyre_classDescriptors:
        # get the descriptor
        descriptor = getattr(Group, name)
        # represent
        channel.line(f"    {name}: {descriptor.type}")
        # the doc string
        channel.line(f"      doc: {descriptor.__doc__}")
        # show me the default value
        channel.line(f"      default: {descriptor.default}")

    # flush
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
