#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that {info.log} works as expected
"""


def test():
    # access the package
    import journal
    # build a info channel
    info = journal.info("journal.test1")
    # activate it
    # info.active = True

    # and make it say something
    info.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
