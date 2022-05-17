#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


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

        id = pyre.h5.int(default=0)


    # configure the journal
    journal.application("pyre.h5.group")
    # make a channel
    channel = journal.debug("pyre.h5.group")

    # show me
    channel.line(f"{Group.__name__}")

    # go through the contents of the identifier map
    channel.line(f"  identifiers:")
    for name, identifier in Group.pyre_idmap.items():
        channel.line(f"    {name}: {identifier}")

    # flush
    channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
