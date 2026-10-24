#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that has read its dictionary keeps it when a key is dropped from the class
dictionary, as with a python cached property
"""


def test() -> None:
    """
    Make an instance, read its dictionary, assign a dictionary with a key missing to the class, and
    read the instance again
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
    # that has seen the class dictionary
    assert dict(b.t) == {"a": 1, "b": 2}
    # drop a key from the class
    base.t = {"a": 1}
    # the instance keeps what it read
    assert dict(b.t) == {"a": 1, "b": 2}
    # while an instance made after the change does not have it
    assert dict(base(name="c").t) == {"a": 1}

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
