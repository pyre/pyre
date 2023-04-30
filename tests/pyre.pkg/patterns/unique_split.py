#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that subclasses can register their own instances in separate registries
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

    class Derived(Base, pyre_unique=True):

        # metamethods
        def __init__(self, name, value=None, **kwds):
            # chain up
            super().__init__(name=name, **kwds)
            # save the value
            self.value = value
            # all done
            return

        @classmethod
        def pyre_hashInstance(self, name, value):
            # hash another constructor argument into the instance key
            return f"{name}.{value}"


    # get the twp registries
    baseReg = Base.pyre_unique
    derivedReg = Derived.pyre_unique
    # verify that they are not the same object
    assert baseReg is not derivedReg

    # make a base instance
    b = Base(name="b")
    # verify it is in the registry
    assert "b" in baseReg
    # but not on the drived registry
    assert "b" not in derivedReg

    # make a derived instance
    d = Derived(name="d", value=2)
    # and another by the same name
    alias = Derived(name="d", value=2)
    # verify that the derived registry has only one entry
    assert len(derivedReg) == 1
    # and that our instance is there
    assert "d.2" in derivedReg

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
