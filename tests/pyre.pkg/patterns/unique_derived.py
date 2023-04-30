#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that instances of subclasses are also registered correctly
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

    class Derived(Base):

        # metamethods
        def __init__(self, name, value=None, **kwds):
            # chain up
            super().__init__(name=name, **kwds)
            # save the value
            self.value = value
            # all done
            return


    # make an instance
    d = Derived(name="d")
    # and another by the same name, accidentally asking for it through the base class
    alias = Base(name="d")

    # verify that they are identical
    assert d is alias

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
