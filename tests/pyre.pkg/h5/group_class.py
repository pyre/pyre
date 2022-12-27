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

    # verify that my table of identifiers is accessible
    identifiers = Group.pyre_identifiers
    # and of the correct size
    assert len(identifiers) == 2
    # check the contents
    assert identifiers["id"].typename == "int"
    assert identifiers["pols"].typename == "list"

    # configure the journal
    journal.application("pyre.h5.group")
    # make a channel
    channel = journal.debug("pyre.h5.group")

    # sign on
    channel.line(f"group: {Group.__name__}")

    # identifier section
    channel.line(f"  identifiers:")
    # go through the contents of the identifier map
    for name, identifier in Group.pyre_identifiers.items():
        # represent
        channel.line(f"    {name}: {identifier}")
        # the doc string
        channel.line(f"      doc: {identifier.pyre_doc}")
        # show me the default value
        channel.line(f"      default: {identifier.default}")

    # flush
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
