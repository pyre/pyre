#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that firewall channels by the same name share a common state
"""


def test():
    # access the package
    import journal
    # build a firewall channel
    firewall = journal.firewall("journal.test1")
    # deactivate it
    firewall.active = False

    # and make it say something
    firewall.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
