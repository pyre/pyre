#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Sanity check: verify that the application namespace is built properly
"""


def test():
    # get access to the framework
    import pyre

    # declare a trivial application
    class application(pyre.application, prefix='sample'):
        """A trivial pyre application"""

    # instantiate
    app = application()

    # verify that the filesystem attribute was set
    assert(app.pfs)
    # and that it is correctly mounted
    assert(app.pfs == app.vfs["/sample"])

    # check the namespace
    assert(app.vfs["/sample/system"])
    assert(app.vfs["/sample/user"])

    return app


# main
if __name__ == "__main__":
    test()


# end of file 
