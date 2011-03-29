#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the application namespace is built properly
"""


def test():
    # get access to the framework
    import pyre.shells

    # declare a trivial application
    class application(pyre.shells.application, family="sample"):
        """A trivial pyre application"""

    # instantiate
    app = application(name="app")

    # verify that the filesystem attribute was set
    assert(app.pyre_filesystem)
    # and that it is correctly mounted
    assert(app.pyre_filesystem == app.fileserver["/sample"])

    # check the namespace
    assert(app.fileserver["/sample/system"])
    assert(app.fileserver["/sample/user"])

    return


# main
if __name__ == "__main__":
    test()


# end of file 
