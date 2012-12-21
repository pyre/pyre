#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise host configuration
"""


def test():
    # externals
    import pyre

    # derive an application class
    class app(pyre.component):
        """sample application"""

        # my host
        host = pyre.platforms.platform()


    # instantiate
    one = app(name='one')
    # check i have a host
    print(one.host)
    assert one.host
    # and return
    return one


# main
if __name__ == "__main__":
    test()


# end of file 
