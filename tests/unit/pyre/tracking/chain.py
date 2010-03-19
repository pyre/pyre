# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that locators can be chained correctly
"""


def script():
    import pyre.tracking

    first = pyre.tracking.newSimpleLocator(source="first")
    second = pyre.tracking.newSimpleLocator(source="second")
    chain = pyre.tracking.chain(this=first, next=second)

    assert str(chain) == "first via second"

    return chain


# main
if __name__ == "__main__":
    script()


# end of file 
