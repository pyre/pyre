#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that classes can intercept instance hashing and provide a custom key
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

        # implementation details
        # this must be a class method so it can override the implementation in the metaclass
        @classmethod
        def pyre_hashInstance(cls, name, **kwds):
            """
            Customize the hash key
            """
            # make a simple modification
            return f"#{name}"


    # make an instance
    b = Base(name="b")
    # and another by the same name
    alias = Base(name="b")

    # verify that they are identical
    assert b is alias
    # get the registry
    registry = Base.pyre_unique
    # verify that it has only one instance
    assert len(registry) == 1
    # and that our key is in it
    assert "#b" in registry

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
