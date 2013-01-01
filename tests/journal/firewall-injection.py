#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify that {firewall.log} works as expected
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
