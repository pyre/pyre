#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def declare():
    """
    Declare a component that records what its traits held while it was being built
    """
    # get the framework
    import pyre

    # make a component
    class component(pyre.component, family="sample.nameless"):
        """
        A test component
        """

        # a string, with an alias
        p1 = pyre.properties.str()
        p1.default = "p1"
        p1.aliases = {"first"}

        # an integer
        p2 = pyre.properties.int()
        p2.default = 0

        # the configuration hook
        def pyre_configured(self, **kwds):
            """
            Record what the traits held when the hook ran
            """
            # remember the values of the traits
            self.seen = (self.p1, self.p2)
            # chain up
            yield from super().pyre_configured(**kwds)
            # all done
            return

        # meta method
        def __init__(self, extra=None, **kwds):
            # chain up
            super().__init__(**kwds)
            # the trait values are in place by now
            self.initialized = (self.p1, self.p2)
            # and so is the argument that is not a trait
            self.extra = extra
            # all done
            return

    # and publish it
    return component


def test():
    """
    Verify that an anonymous component instance accepts trait values as constructor arguments,
    under any of their spellings, and that they are in place before the configuration hooks run
    """
    # get the declaration
    component = declare()

    # an anonymous instance built with trait values and an ordinary argument
    c = component(p1="one", p2="2", extra="x")
    # it is anonymous
    assert c.pyre_name is None
    # the values landed, converted to their types: the string
    assert c.p1 == "one"
    # and the integer
    assert c.p2 == 2
    # the configuration hook saw them
    assert c.seen == ("one", 2)
    # and so did the constructor
    assert c.initialized == ("one", 2)
    # while the ordinary argument reached the constructor untouched
    assert c.extra == "x"

    # the alias spelling works as well
    d = component(**{"first": "alias"})
    # for the trait it names
    assert d.p1 == "alias"
    # and leaves the other one alone
    assert d.p2 == 0

    # an instance built without arguments
    e = component()
    # gets the default string
    assert e.p1 == "p1"
    # and the default integer
    assert e.p2 == 0
    # and so does its configuration hook
    assert e.seen == ("p1", 0)

    # instances are independent of each other: the first one
    assert c.p1 == "one"
    # and the second
    assert d.p1 == "alias"

    # and a named instance takes them the same way
    n = component(name="nameless-named", p1="named", p2=7)
    # it has its name
    assert n.pyre_name == "nameless-named"
    # its string
    assert n.p1 == "named"
    # its integer
    assert n.p2 == 7
    # and its configuration hook saw both
    assert n.seen == ("named", 7)

    # all done
    return c


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
