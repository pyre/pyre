#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that {error.log} works as expected
"""


def test():
    # access the package
    import journal
    # build a error channel
    error = journal.error("journal.test1")
    # deactivate it
    error.active = False

    # and make it say something
    error.log("hello world!")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 
