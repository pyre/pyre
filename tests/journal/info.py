#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that info channels by the same name share a common state
"""


def test():
    # access the package
    import journal
    # build a info channel
    info = journal.info("journal.test1")
    # verify that it is off by default
    assert info.active == False
    # enable it
    info.active = True

    # access the same channel through another object
    clone = journal.info("journal.test1")
    # verify that it is now on
    assert clone.active == True

    # build a info channel with a different name
    another = journal.info("journal.test2")
    # verify that it is off by default, to make sure that there is no crosstalk between channels
    assert another.active == False

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
