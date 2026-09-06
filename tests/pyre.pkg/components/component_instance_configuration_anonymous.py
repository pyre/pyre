#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an anonymous component instance accepts trait values as constructor arguments, under
any of their spellings, and that they are in place before the configuration hooks run
"""


def declare():
    # get the framework
    import pyre

    # make a component
    class component(pyre.component, family="sample.nameless"):
        """a test component"""

        # properties
        p1 = pyre.properties.str(default="p1")
        p1.aliases = {"first"}
        p2 = pyre.properties.int(default=0)

        # the configuration hook
        def pyre_configured(self, **kwds):
            # record what the traits held when the hook ran
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
    # get the declaration
    component = declare()

    # an anonymous instance built with trait values and an ordinary argument
    c = component(p1="one", p2="2", extra="x")
    # it is anonymous
    assert c.pyre_name is None
    # the values landed, converted to their types
    assert c.p1 == "one"
    assert c.p2 == 2
    # the configuration hook saw them
    assert c.seen == ("one", 2)
    # and so did the constructor
    assert c.initialized == ("one", 2)
    # while the ordinary argument reached the constructor untouched
    assert c.extra == "x"

    # the alias spelling works as well
    d = component(**{"first": "alias"})
    assert d.p1 == "alias"
    assert d.p2 == 0

    # an instance built without arguments gets the defaults
    e = component()
    assert e.p1 == "p1"
    assert e.p2 == 0
    assert e.seen == ("p1", 0)

    # instances are independent of each other
    assert c.p1 == "one"
    assert d.p1 == "alias"

    # and a named instance behaves as it always did
    n = component(name="nameless-named", p1="named", p2=7)
    assert n.pyre_name == "nameless-named"
    assert n.p1 == "named"
    assert n.p2 == 7
    assert n.seen == ("named", 7)

    # all done
    return c


# main
if __name__ == "__main__":
    test()


# end of file
