#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to a class dictionary reaches an existing instance, as with python classes
"""


def test() -> None:
    """
    Make an instance, assign a dictionary with new values to the class, and read the instance
    """
    # access the framework
    import pyre

    # a component class with a dictionary
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a dictionary"""

        # the dictionary, with its class default
        t = pyre.properties.dict(schema=pyre.properties.int(), default={"a": 1, "b": 2})

    # an instance made before the change
    b = base(name="b")
    # change the values of the class
    base.t = {"a": 10, "b": 20}
    # the instance sees the new values
    assert dict(b.t) == {"a": 10, "b": 20}

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
