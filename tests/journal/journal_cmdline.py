#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre # this should be removable after journal is properly implemented

    # dump the configuration store
    pyre.executive.configurator.dump("journal")

    # now declare a class in the {journal} namespace
    class Journal(pyre.component, family="journal"):
        """
        Configuration thief
        """
    
    # instantiate
    j = Journal(name="journal")

    # dump the configuration store again
    pyre.executive.configurator.dump("journal")
    # and any errors
    for error in pyre.executive.errors:
        print(error)

    return


# main
if __name__ == "__main__":
    test()


# end of file 
