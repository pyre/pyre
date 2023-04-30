#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the simplest use case works as expected
    """
    # access
    from pyre.patterns.Unique import Unique

    # declare a class with an instance registry
    class Base(metaclass=Unique):

        # metamethods
        def __init__(self, name, **kwds):
            # chain up
            super().__init__(**kwds)
            # save the name
            self.name = name
            # all done
            return

    # make an instance
    b = Base(name="b")
    # and another by the same name
    alias = Base(name="b")

    # verify that they are identical
    assert b is alias

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
